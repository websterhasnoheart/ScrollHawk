import os
import sys
from pyfiglet import Figlet
from pathlib import Path


myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
abs_path = str(path.parent.absolute())
sys.path.append(abs_path)


def zk_main_menu():
    pass