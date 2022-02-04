import argparse

# Main parser
parser = argparse.ArgumentParser(prog='eldensave',
                                 description='savegame manager for Elden Ring')
parser.add_argument('-r', '--revert', )

# Define subparsers
subparsers = parser.add_subparsers()

# Create a backup of the current save file
save_parser = subparsers.add_parser('save',
                                    description='use this command for saving the current savegame in a backup')
save_parser.add_argument('-b' '--backup',
                         help='create temporary backup save (that you know is not broken)',
                         action='store_true')

# Restore a save from one of the backups
restore_parser = subparsers.add_parser('restore',
                                       description='use this command for replacing the current savegame with a backup')
restore_parser.add_argument('-rb' '--restore-backup',
                            help='restore your temporary backup save',
                            action='store_true')

# TODO: Use set_defaults() to map to functions/dest names so SaveManager can know which mode its in