from SaveManager import SaveManager
from Parser import ArgParser


def main():
    elden_parser = ArgParser()
    elden_args = elden_parser.get_args()
    save_manager = SaveManager(custom_loc=elden_args.custom,
                               args=elden_args,
                               mode=elden_parser.get_mode()
                               )


if __name__ == '__main__':
    main()
