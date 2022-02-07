import psutil
import getpass
from pathlib import Path
import shutil
import os
import pickle

SAVE_DIR = 'saves/'
SAVE_DATA = SAVE_DIR + 'savedata'

"""
Save Manager

- add function to restore automatic temporary backup
- flush temporaries if file name changes?
- change custom -c flag logic to be more intuitive
"""
class SaveManager:
    def __init__(self,
                 mode,
                 args,
                 custom_loc=False,
                 ):
        self.__user = getpass.getuser()
        self.save_path = None
        self.mode = mode
        self.args = args
        self.saves = {}
        self.save = None

        # Load current save data
        self.__unpickle_saves()
        if not self.saves:
            print('Save data currently empty...')

        # List all current saves
        if self.args.list:
            self.print_user_saves()

        # Create custom directory structure for storing saves
        # RECREATE ENTIRE STRUCTURE?
        self.__create_save_dirs()

        # If custom location flag
        if not custom_loc:
            self.save_path = self.get_save_path()
        else:
            with open('game_savepath.txt', 'r') as f:
                self.save_path = Path(f.read().strip().lstrip('/'))

        self.create_backup()  # Create every time program runs

        # TODO: move a lot of this logic into helper functions
        if self.mode == 'load':
            if self.args.lb__load_backup:
                self.load_backup('userbackup')
            else:
                save_name = self.__get_inputted_savename()
                print(f'loading {save_name}...')
                self.load_backup(save_name)
                print(f'{save_name} loaded!')
        elif self.mode == 'save':
            if self.args.b__backup:
                self.create_backup('userbackup')
            else:
                save_name = self.__get_inputted_savename()
                save_description = input('Please enter a brief description of your save: ').strip()
                self.save = self.create_save(save_name, save_description)
                self.saves[save_name] = self.save
                self.__pickle_saves()
                print(f'{save_name} created!')
        elif self.mode == 'remove':
            saves_to_remove = self.args.savenames
            if not saves_to_remove:
                print('(unimplemented)')
            else:
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

    def create_save(self, name, description):
        return SaveManager.Save(outer_instance=self, name=name, description=description)

    """
    Retrieves expected location or asks user to input custom location of their savegame
    """
    def get_save_path(self) -> Path:
        custom = False
        print('Checking default game save location...')

        path = Path(f'C:/Users/{self.__user}/AppData/Roaming/GAME_NAME/path/to/savefile.file')
        while not path.exists():
            custom = True
            path = Path(input(('Could not find savegame folder at default location, please enter the full path of'
                               'your savegame folder (q to quit): ')))
            if str(path).strip().startswith('q'):
                print('Exiting...')
                exit(0)
        if custom:
            print('Storing new game save location...')
            with open('game_savepath.txt', 'w') as f:
                f.write(str(path))
        print('Save location found!')
        return path

    def print_user_saves(self):
        print('Saves:')
        for save in self.saves.values():
            print(str(save))

    def create_backup(self, mode='temporary'):
        save_name = self.format_file_name(self.save_path)
        os.makedirs(os.path.dirname(SAVE_DIR + f'/{mode}/' + save_name), exist_ok=True)
        shutil.copyfile(self.save_path, SAVE_DIR + f'/{mode}/' + save_name)

    def load_backup(self, save='temporary'):
        save_name = self.format_file_name(self.save_path)
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        shutil.copyfile(SAVE_DIR + f'/{save}/' + save_name, self.save_path)

    def __load(self):
        pass

    def __save(self):
        pass

    def __remove(self):
        pass

    def __unpickle_saves(self):
        if os.path.getsize(SAVE_DATA) > 0:
            with open(SAVE_DATA, "rb") as f:
                self.saves = pickle.load(f)

    def __pickle_saves(self):
        with open(SAVE_DATA, "wb") as f:
            pickle.dump(self.saves, f)

    def __get_inputted_savename(self):
        save_name = self.args.savename
        if not save_name:
            save_name = input('Please enter the name of your save: ').strip()
        return save_name

    @staticmethod
    def __create_save_dirs():
        try:
            os.mkdir('saves/')
        except FileExistsError:
            # Save structure already exists, so no need to create
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
