import getpass
import zipfile
import zlib
import os
import pickle
import shutil
import sys
import re
from pathlib import Path
import psutil
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Change working directory to current directory to utilize relative paths more easily
os.chdir(sys.path[0])

# Internal folders/files/globals to manage save data
SAVE_DIR = 'saves/'
SAVE_DATA = SAVE_DIR + 'savedata'
GAMES = {'Dark Souls 3': 'DarkSoulsIII', 'Elden Ring': 'EldenRing', 'Sekiro': 'Sekiro'}
GAME_NAMES = GAMES.keys()

# TODO: Interfacing, reorganize functions to avoid repeated code in GUI section
class SaveManager:
    """
    Save Manager
    gui: runs graphical user interface
    save, remove, load: run command line interface
    """

    def __init__(self,
                 mode,
                 args,
                 custom_loc=False,
                 ):
        self.__user = getpass.getuser()
        self.__loc = custom_loc
        self.save_path = None
        self.mode = mode
        self.args = args
        self.saves = {}
        self.save = None
        self.game = 'Dark Souls 3'

    def start(self):
        # Load current save data from serialized savedata
        self.__unpickle_saves()

        # Create custom directory structure for storing saves
        self.__create_save_dirs()

        # List all current user saves
        if self.args.list:
            self.print_user_saves()

        # If custom location flag, set the game's save location to the user's input
        if not self.__loc:
            self.save_path = self.__get_save_path()
        else:
            with open('game_savepath.txt', 'r') as f:
                self.save_path = Path(f.read().strip().lstrip('/'))
                if not self.save_path.exists():
                    print('Custom savefile location does not exist, exiting...')
                    exit(1)

        self.create_backup()  # Create every time program runs

        print(f'**Current game: {self.game}**\n')

        # If --cli flag is false, set up GUI
        if self.mode == 'gui':
            print('GUI mode selected')
            self.start_gui()
        else:
            print('CLI mode selected\n')
            if self.mode == 'load':
                self.__load()
            elif self.mode == 'save':
                self.__save()
            elif self.mode == 'remove':
                self.__remove()

    # TODO: break up this function
            # outer keys to store game names in saves object data, use based on current game
            # Add progress/success message and error messages
            # Add image that changes based on name
            # Reformat positioning
            # Wrap getting save name in function
            # Refactor and interface
    def start_gui(self):
        print('Running...')

        def save():
            if use_temporary.get():
                self.create_backup('userbackup')
                messagebox.showinfo('Success', 'Temporary backup saved!')
            else:
                save_value = None
                for i in listbox.curselection():
                    save_value = listbox.get(i)
                if not save_value:
                    save_value = new_save_name.get()
                save_desc = 1  # new_save_desc.get() # TODO: figure out description
                if save_value:
                    new_save_object = self.create_save(save_value, save_desc)
                    self.saves[save_value] = new_save_object
                    self.__pickle_saves()
                    messagebox.showinfo('Success', f'{save_value} saved!')
                    update_savelist()

        def load():
            if use_temporary.get():
                self.load_backup('userbackup')
                messagebox.showinfo('Success', 'Temporary backup loaded!')
            else:
                save_value = None
                for i in listbox.curselection():
                    save_value = listbox.get(i)
                if save_value:
                    self.load_backup(save_value)
                    messagebox.showinfo('Success', f'{save_value} load!')
                    update_savelist()

        def remove():
            save_value = None
            for i in listbox.curselection():
                save_value = listbox.get(i)
            if save_value:
                # TODO: extract save name from save_value (which is a name/desc combo)
                print(f'deleting {save_value}...')
                del self.saves[save_value]
                shutil.rmtree(SAVE_DIR + save_value)
                messagebox.showinfo('Success', f'{save_value} deleted!')
                # Re-pickle save data to reflect update
                self.__pickle_saves()
                update_savelist()
            else:
                messagebox.showinfo('Failure', 'You must select a save to delete')

        def kill():
            print('Exiting...')
            root.destroy()

        # Callback function for updating clickable buttons
        # TODO: Split into individual callback functions for check box and listbox
        def update_buttons(event=None):
            save_value = None
            for i in listbox.curselection():
                save_value = listbox.get(i)
            if use_temporary.get() or save_value:
                save_btn['state'] = NORMAL
                load_btn['state'] = NORMAL
                remove_btn['state'] = NORMAL if save_value else DISABLED
            else:
                save_btn['state'] = DISABLED
                load_btn['state'] = DISABLED
                remove_btn['state'] = DISABLED

        # Turns on Save button if user inputted a new save name
        def validate_new_save():
            if new_save_name.get():
                save_btn['state'] = NORMAL
                return True
            else:
                update_buttons()
                return False

        # Callback function to run whenever a save is saved or removed
        def update_savelist():
            saves = listbox.get(0, END)
            for i, save_object in enumerate(self.saves.values()):
                if str(save_object) not in saves:
                    listbox.insert(i, save_object.name + f': {save_object.description}')

        # Set up GUI window root and main frame
        root = Tk()
        root.title('SoulsSave')
        root.geometry("500x400")
        frame = Frame(root)
        frame.pack()

        # Main menu
        main_menu = Menu(frame)
        main_menu.add_command(label="Exit", command=kill)
        root.config(menu=main_menu)

        saves_label = Label(root, text="Your Saves")
        saves_label.pack()

        # Frame for saves
        saves_frame = Frame(root)
        saves_frame.pack()

        listbox = Listbox(saves_frame, width=50, height=10)

        # Generate with for loop over list of serialized saves by name
        update_savelist()
        listbox.bind('<<ListboxSelect>>', update_buttons)

        # Set up horizontal and vertical scroll bars
        listbox_sb = Scrollbar(saves_frame, orient=HORIZONTAL)
        listbox_vb = Scrollbar(saves_frame, orient=VERTICAL)
        listbox_sb.pack(fill=X, side=BOTTOM)
        listbox_vb.pack(fill=Y, side=RIGHT)
        listbox.configure(xscrollcommand=listbox_sb.set, yscrollcommand=listbox_vb.set)
        listbox_sb.config(command=listbox.xview)
        listbox_vb.config(command=listbox.yview)
        listbox.pack()

        # Game select combobox (normalize with game list in SaveManager)
        # Also need a load_image() function to change the image based on the game
        game_list = ["Elden Ring", "Sekiro", "Dark Souls III"]

        game_combobox = ttk.Combobox(frame, values=game_list)
        game_combobox.set(self.game)
        game_combobox.pack(padx=5, pady=5)

        # Add checkbox for temporary saves
        use_temporary = BooleanVar()
        temporary_btn = Checkbutton(frame, width=15, variable=use_temporary, text='Temporary Save', command=update_buttons)
        temporary_btn.pack(padx=5, pady=5)

        # New save
        new_save_name = StringVar()
        new_save = Entry(frame, width=20, textvariable=new_save_name, validate="focusout", validatecommand=validate_new_save)
        new_save.insert(0, 'new save name')
        new_save.pack(padx=5, pady=5)

        new_save_desc = Text(frame, width=20, height=3)
        new_save_desc.insert(END, 'save description')
        new_save_desc.pack(padx=5, pady=5)

        # Load button
        load_btn = Button(frame, text='Load', state=DISABLED, padx=20, pady=5, command=load)
        load_btn.pack(side=RIGHT, padx=5, pady=5)

        # Save button
        save_btn = Button(frame, text='Save', state=DISABLED, padx=20, pady=5, command=save)
        save_btn.pack(side=RIGHT, padx=5, pady=5)

        # Remove button
        remove_btn = Button(frame, text='Remove', state=DISABLED, padx=20, pady=5, command=remove)
        remove_btn.pack(side=RIGHT, padx=5, pady=5)

        # Start GUI loop
        root.mainloop()

    def create_save(self, name, description):
        return SaveManager.Save(outer_instance=self, name=name, description=description)

    def print_user_saves(self):
        print('Saves:')
        if not self.saves:
            print('Save data currently empty...')
        else:
            for save in self.saves.values():
                print(str(save))
        print(75 * '-')

    def create_backup(self, mode='temporary'):
        save_name = self.format_file_name(self.save_path)
        path = SAVE_DIR + f'/{mode}/' + save_name
        # Compression (need to pass .zip file)
        self.__compress_folder(self.save_path, path + '.zip')

    def load_backup(self, save='temporary'):
        save_name = self.format_file_name(self.save_path)
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        path = SAVE_DIR + f'/{save}/' + save_name
        try:
            self.__uncompress_folder(self.save_path, path + '.zip')
            if save == 'userbackup':
                print('Temporary backup loaded!')
            else:
                print(f'{save} loaded!')
        except FileNotFoundError:
            if save == 'userbackup':
                print('You do not have a temporary backup currently saved!')
            else:
                print(f'You do not have a save called "{save}"')

    def __load(self):
        if self.args.b__backup:
            self.load_backup('userbackup')
        else:
            save_name = self.__get_inputted_savename()
            print(f'loading {save_name}...')
            self.load_backup(save_name)

    def __save(self):
        if self.args.b__backup:
            print('Creating temporary backup...')
            self.create_backup('userbackup')
            print('Created user backup!')
        else:
            save_name = self.__get_inputted_savename()
            save_description = input('Please enter a brief description of your save: ').strip()
            self.save = self.create_save(save_name, save_description)
            self.saves[save_name] = self.save
            self.__pickle_saves()
            print(f'{save_name} created!')

    def __remove(self):
        saves_to_remove = self.args.savenames
        if not saves_to_remove:
            saves_to_remove = self.__get_inputted_savename().split()
        for save in saves_to_remove:
            # Remove from current save data
            if save not in self.saves:
                print(f'{save} is not one of your saves, skipping...')
            else:
                print(f'deleting {save}...')
                del self.saves[save]
                shutil.rmtree(SAVE_DIR + save)
                print(f'{save} deleted')
            # Re-pickle save data to reflect update
            self.__pickle_saves()
        print('done deleting saves!')

    def __unpickle_saves(self):
        """
        Read custom save data from file
        """
        if os.path.getsize(SAVE_DATA) > 0:
            with open(SAVE_DATA, "rb") as f:
                self.saves = pickle.load(f)

    def __pickle_saves(self):
        """
        Serialize custom save data to a file to be read from later
        """
        with open(SAVE_DATA, "wb") as f:
            pickle.dump(self.saves, f)

    def __get_save_path(self) -> Path:
        """
        Retrieves expected location or asks user to input custom location of their savegame
        """
        custom = False
        print('Checking default game save location...')
        game = GAMES[self.game]
        path = Path(f'C:/Users/{self.__user}/AppData/Roaming/{game}/')
        while not path.exists():
            custom = True
            path = Path(input(('Could not find savegame folder at current path, please enter the full path of '
                               'the savegame folder (q to quit): ')))
            if str(path).strip().startswith('q'):
                print('Exiting...')
                exit(0)
            # Check for GraphicsConfig file and 17-digit Steam ID to verify folder
            if os.path.exists(f'{path}/GraphicsConfig.xml') and len(
                    re.findall(r'\d{17}', str(os.listdir(path)))) > 0:
                break
            else:
                print('Cant find savedata in this Directory. The selected folder should contain GraphicsConfig.xml '
                      'and a folder named after your 17 digit SteamID')
                continue
        if custom:
            print('Storing new game save location...')
            with open('game_savepath.txt', 'w') as f:
                f.write(str(path))
        print('Save location found!')
        return path

    def __get_inputted_savename(self):
        if self.mode == 'remove':
            save_name = self.args.savenames
        else:
            save_name = self.args.savename
        if not save_name:
            save_name = input('Please enter the name of your save(s): ').strip()
        return save_name

    @staticmethod
    def __create_save_dirs():
        try:
            os.mkdir('saves/')
        except FileExistsError:
            # Save structure already exists, so no need to create save folder
            pass

    @staticmethod
    def check_process_running(process_name):
        """
        Check if there is any running process that contains the given name processName.
        """
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    @staticmethod
    def format_file_name(file):
        formatted = str(file).split('\\')[-1]
        return formatted

    @staticmethod
    def __compress_folder(gamesave_path: Path, usersave_path: str):
        with zipfile.ZipFile(usersave_path, mode='w', compression=zipfile.ZIP_DEFLATED) as usersave_zip:
            for file_path in gamesave_path.rglob('*'):
                usersave_zip.write(file_path, arcname=file_path.relative_to(gamesave_path))

    @staticmethod
    def __uncompress_folder(gamesave_path: Path, usersave_path: str):
        with zipfile.ZipFile(usersave_path, mode='r', compression=zipfile.ZIP_DEFLATED) as usersave_zip:
            usersave_zip.extractall(gamesave_path)

    """
    Represents an individual save
    """
    class Save:
        def __init__(self,
                     outer_instance,
                     name,
                     description):
            self.outer_instance = outer_instance
            self.name = name
            self.description = description
            self.__make_directory()
            self.save_file()

        def __str__(self):
            return f'{self.name}: {self.description}'

        def __make_directory(self):
            path = SAVE_DIR + self.name
            try:
                os.mkdir(path)
            except FileExistsError:
                print('You have already created a save with this name!')
                overwrite = input("Would you like to overwrite this save? (y/n): ").strip()
                while overwrite:
                    if overwrite == 'n':
                        print('Exiting...')
                        exit(0)
                    elif overwrite == 'y':
                        shutil.rmtree(path)
                        os.mkdir(path)
                        break
                    else:
                        print('Please enter y or n: ')

        def save_file(self):
            self.outer_instance.create_backup(self.name)
