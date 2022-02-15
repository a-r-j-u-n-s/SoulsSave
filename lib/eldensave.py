from SaveManager import SaveManager
from Parser import ArgParser


def main():
    parser = ArgParser()
    args = parser.get_args()
    save_manager = SaveManager(custom_loc=args.custom,
                               args=args,
                               mode=parser.get_mode()
                               )
    save_manager.start()


if __name__ == '__main__':
    main()
