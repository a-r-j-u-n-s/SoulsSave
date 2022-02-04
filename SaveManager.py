import psutil
import getpass
from pathlib import Path
from Parser import parser, save_parser, restore_parser

"""
Save Manager

- creates invisible temporary backup whenever restore is used, revert feature if it breaks
"""
class SaveManager:
    def __init__(self,
                 custom_loc=False):
        self.user = getpass.getuser()
        self.save_path = None
        self.args = parser.parse_args()
        self.save_args = save_parser.parse_args()
        self.restore_args = restore_parser.parse_args()
        self.mode = None

        # Set current mode

        # If custom location flag (need to set up this logic in the parser and in main.py somehow
        if not custom_loc:
            self.save_path = self.get_save_path()
        else:
            with open('eldenring_savepath', 'r') as f:
                self.save_path = Path(f.read().strip())


    def get_save_path(self) -> Path:
        """
        Retrieves expected location or asks user to input custom location of their savegame
        """
        custom = False
        print('Checking default Elen Ring save location...')

        path = Path(f'C:/Users/{self.user}/AppData/Roaming/EldenRing/')
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

    class Save:
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
