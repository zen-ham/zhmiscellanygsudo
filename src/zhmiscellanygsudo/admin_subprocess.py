from ._supportfuncs import _gsudo_binary_path
import subprocess


def run(command, keep_same_console=True, **kwargs):
    if type(command) == list:
        command.insert(0, _gsudo_binary_path)
        if not keep_same_console:
            command.insert(0, "-n")
    elif type(command) == str:
        command = f'{_gsudo_binary_path}{" -n" if not keep_same_console else ""} {command}'
    else:
        raise TypeError(f'Invalid command type "{type(command)}" for zhmiscellanygsudo.run, requires list or str')
    process = subprocess.run(command, **kwargs)
    return process


def Popen(command, **kwargs):
    if type(command) == list:
        command.insert(0, _gsudo_binary_path)
    elif type(command) == str:
        command = f'{_gsudo_binary_path} {command}'
    else:
        raise TypeError(f'Invalid command type "{type(command)}" for zhmiscellanygsudo.Popen, requires list or str')
    process = subprocess.run(command, **kwargs)
    return process
