import psutil
import getpass
from pathlib import Path
import shutil

"""
Save Manager

- creates invisible temporary backup whenever restore is used, revert feature if it breaks
"""
class SaveManager:
    def __init__(self,
                 mode,
                 args,
                 custom_loc=False
                 ):
        self.__user = getpass.getuser()
        self.save_path = None
        self.mode = mode
        self.args = args
        self.saves = []     # List of Save objects

        # If custom location flag
        if not custom_loc:
            self.save_path = self.get_save_path()
        else:
            with open('eldenring_savepath.txt', 'r') as f:
                self.save_path = Path(f.read().strip().lstrip('/'))

        self._saves_path = 'saves/'    # Path to internal save/backup data

        self.__create_temporary_backup()    # Create every time program runs

    def create_save(self, ):

    def get_save_path(self) -> Path:
        """
        Retrieves expected location or asks user to input custom location of their savegame
        """
        custom = False
        print('Checking default Elen Ring save location...')

        path = Path(f'C:/Users/{self.__user}/AppData/Roaming/EldenRing/')
        while not path.exists():
            custom = True
            path = Path(input(('Could not find savegame folder at default location, please enter the full path of'
                               'your savegame folder (q to quit): ')))
            if str(path).strip().startswith('q'):
                print('Exiting...')
                exit(0)
        if custom:
            print('Saving new Elden Ring save location...')
            with open('eldenring_savepath', 'w') as f:
                f.write(str(path))
        print('Save location found!')
        return path

    """
    Represents an individual save
    """
    class Save:
        def __init__(self):


    def __create_temporary_backup(self):
        save_name = self.format_file_name(self.save_path)
        shutil.copyfile(self.save_path, self._saves_path + '/temporary/' + save_name)

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
