import os, zhmiscellany, sys


def get_gsudo_binary_path():
    anyway = False
    if getattr(sys, 'frozen', False):
        # we are running in a PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # we are running in normal Python environment
        base_path = os.path.dirname(__file__)
        state_path = os.path.join(base_path, '_state.py')
        if os.path.exists(state_path):
            with open(state_path, 'r') as f:
                state = f.read()
            if state == '_state=0':
                with open(state_path, 'w') as f:
                    f.write('_state=1')
                anyway = True

    cwd = os.getcwd()
    if (not os.path.exists(os.path.join(base_path, 'resources'))) or anyway:
        if os.path.exists(os.path.join(base_path, 'resources')):
            zhmiscellany.fileio.remove_folder(os.path.join(base_path, 'resources'))
        os.chdir(base_path)
        from ._py_resources import gen
        gen()
        os.chdir(cwd)
    return os.path.join(base_path, 'resources', 'x64', 'gsudo.exe')


_gsudo_binary_path = get_gsudo_binary_path()


def rerun_as_admin(keep_same_console=True):
    pass
