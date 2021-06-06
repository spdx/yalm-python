import os
from pathlib import Path, PureWindowsPath, PurePosixPath

path_home = str(PureWindowsPath(Path.home()))
path_home = os.path.abspath(os.path.dirname(__file__))
path_home = os.path.join(path_home, os.pardir)

PACKAGE_PATH = str(PureWindowsPath(path_home))
PACKAGE_PATH = PACKAGE_PATH.replace('\\', os.sep)
PACKAGE_PATH = str(Path(PACKAGE_PATH))
