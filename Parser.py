import argparse

MODES = ['load', 'save', 'remove']


class ArgParser:
    def __init__(self):
        # Main parser
        self.parser = argparse.ArgumentParser(prog='eldensave',
                                              description='savegame manager for Elden Ring')
        self.parser.add_argument('-c', '--custom', help='set Steam game save location manually in file',
                                 action='store_true')
        self.parser.add_argument('-l', '--list', help='list all current saves', action='store_true')

        # Define subparsers
        subparsers = self.parser.add_subparsers(dest='mode')

        # Create a backup of the current save file
        save_parser = subparsers.add_parser('save',
                                            help='use this command for saving the current savegame in a backup',
                                            description='use this command for saving the current savegame in a backup')
        save_parser.add_argument('-b' '--backup',
                                 help='create temporary backup save (that you know is not broken)',
                                 action='store_true')
        save_parser.add_argument('savename',
                                 help='name of save',
                                 nargs='?'
                                 )

        # Restore a save from one of the backups
        load_parser = subparsers.add_parser('load',
                                            help='use this command to replace the current savegame with one of your'
                                                 'saved backups',
                                            description='for replacing the current savegame with '
                                                        'a backup that you saved previously')
        load_parser.add_argument('-lb' '--load-backup',
                                 help='restore your temporary backup save',
                                 action='store_true')

        load_parser.add_argument('savename',
                                 help='name of save you want to load',
                                 nargs='?'
                                 )

        # Restore a save from one of the backups
        remove_parser = subparsers.add_parser('remove',
                                              help='use this command to delete one of your savegames',
                                              description='for deleting savegames')
        remove_parser.add_argument('savenames',
                                   help='name of save you want to delete',
                                   nargs='*')

        self.args = self.parser.parse_args()
        self.mode = self.__set_mode()

    def __set_mode(self):
        if self.args.mode in MODES:
            return self.args.mode
        return None

    def get_args(self):
        return self.args

    def get_parser(self):
        return self.parser

    def get_mode(self):
        return self.mode
