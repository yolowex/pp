from core.common.names import *
from core.app_entry import AppEntry


def main():
    pg.init()
    entry = AppEntry()
    entry.run()


if __name__ == "__main__":
    main()
