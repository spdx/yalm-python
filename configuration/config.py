import os
from pathlib import Path, PureWindowsPath, PurePosixPath

path_home = str(PureWindowsPath(Path.home()))
PACKAGE_PATH = PureWindowsPath(path_home + "\\spdx_python_licensematching")
PACKAGE_PATH = str(PACKAGE_PATH)
PACKAGE_PATH = PACKAGE_PATH.replace('\\',os.sep)
PACKAGE_PATH = str(Path(PACKAGE_PATH))
