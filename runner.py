from interface.main_menu import main_menu
import os

if __name__ == '__main__':
    os.environ['ZK_SYNC_LIBRARY_PATH'] = "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10 site-packages/zksync_sdk/__init__.py"

    main_menu()

