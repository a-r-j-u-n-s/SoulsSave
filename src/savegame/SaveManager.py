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
from tkinter import ttk

# Change working directory to current directory to utilize relative paths more easily
os.chdir(sys.path[0])

# Internal folders/files/globals to manage save data
SAVE_DIR = 'saves/'
SAVE_DATA = SAVE_DIR + 'savedata'
GAMES = {'Dark Souls 3': 'DarkSoulsIII', 'Elden Ring': 'EldenRing', 'Sekiro': 'Sekiro'}
GAME_NAMES = GAMES.keys()


class SaveManager:
    """
    Save Manager
    --cli: runs in CLI mode
    Default mode is GUI
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
        if not self.args.cli:
            print('GUI mode selected\n')
            self.start_gui()
        else:
            print('CLI mode selected\n')
            if self.mode == 'load':
                self.__load()
            elif self.mode == 'save':
                self.__save()
            elif self.mode == 'remove':
                self.__remove()

    def start_gui(self):
        def save():
            print('save mode')

        def load():
            print('load mode')

        root = Tk()
        root.geometry("500x300")
        frame = Frame(root)
        frame.pack()

        mainmenu = Menu(frame)
        mainmenu.add_command(label="Save", command=save)
        mainmenu.add_command(label="Load", command=load)
        mainmenu.add_command(label="Exit", command=root.destroy)

        root.config(menu=mainmenu)

        label = Label(root, text="Your Saves")
        label.pack()

        listbox = Listbox(root)

        # Generate with for loop over list of serialized saves by name
        listbox.insert(1, "Bread")
        listbox.insert(2, "Milk")
        listbox.insert(3, "Meat")
        listbox.insert(4, "Cheese")
        listbox.insert(5, "Vegetables")

        listbox.pack()

        # Game select combobox (normalize with game list in SaveManager)
        # Also need a load_image() function to change the image based on the game
        game_list = ["Elden Ring", "Sekiro", "Dark Souls III"]

        Combo = ttk.Combobox(frame, values=game_list)
        Combo.set(self.game)
        Combo.pack(padx=5, pady=5)

        # Add checkbox for temporary saves
        Var1 = BooleanVar()
        ChkBttn = Checkbutton(frame, width=15, variable=Var1, text='Temporary Save')
        ChkBttn.pack(padx=5, pady=5)

        # New save
        new_save = Entry(frame, width=20)
        new_save.insert(0, 'Enter new save name')
        new_save.pack(padx=5, pady=5)

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
