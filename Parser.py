import argparse

MODES = ['load', 'save']


class ArgParser:
    def __init__(self):
        # Main parser
        self.parser = argparse.ArgumentParser(prog='eldensave',
                                              description='savegame manager for Elden Ring')
        self.parser.add_argument('-c', '--custom', help='set Elden Ring save location manually in file')

        # Define subparsers
        subparsers = self.parser.add_subparsers(dest='mode')

        # Create a backup of the current save file
        save_parser = subparsers.add_parser('save',
                                            help='use this command for saving the current savegame in a backup',
                                            description='use this command for saving the current savegame in a backup')
        save_parser.add_argument('-b' '--backup',
                                 help='create temporary backup save (that you know is not broken)',
                                 action='store_true')

        # TODO: do both?
        # restore_parser = subparsers.add_parser('replace',
        #                                        help='use this command to save and replace the current savegame with one of'
        #                                             'your saved backups ',
        #                                        description='for replacing the current savegame with '
        #                                                    'a backup that you saved previously')

        # Restore a save from one of the backups
        restore_parser = subparsers.add_parser('load',
                                               help='use this command to replace the current savegame with one of your'
                                                    'saved backups',
                                               description='for replacing the current savegame with '
                                                           'a backup that you saved previously')
        restore_parser.add_argument('-lb' '--load-backup',
                                    help='restore your temporary backup save',
                                    action='store_true')

        self.args = self.parser.parse_args()

        self.mode = None
        self.__set_mode()

    def __set_mode(self):
        if self.args.mode in MODES:
            self.mode = self.args.mode

    def get_args(self):
        return self.args

    def get_parser(self):
        return self.parser

    def get_mode(self):
        return self.mode
