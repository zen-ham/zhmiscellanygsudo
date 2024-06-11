from ._supportfuncs import _gsudo_binary_path
import os


def Popen(keep_same_console=True, **kwargs):
    print(_gsudo_binary_path)
    os.path.exists(_gsudo_binary_path)