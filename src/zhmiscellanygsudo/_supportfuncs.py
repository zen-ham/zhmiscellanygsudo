import os, zhmiscellany, sys, ctypes
import zhmiscellanygsudo.admin_subprocess.run
import zhmiscellanygsudo.admin_subprocess.Popen


def get_gsudo_binary_path():
    anyway = False
    if getattr(sys, 'frozen', False):
        # we are running in a PyInstaller bundle
        base_path = sys._MEIPASS
        anyway = True
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
        os.chdir(base_path)
        from ._py_resources import gen
        gen()
        os.chdir(cwd)
    return os.path.join(base_path, 'resources', 'x64', 'gsudo.exe')


_gsudo_binary_path = get_gsudo_binary_path()


def rerun_as_admin(keep_same_console=True):
    if zhmiscellany.misc.is_admin():
        return

    # Get the script path
    if getattr(sys, 'frozen', False):
        # If the script is compiled to an EXE
        script_path = sys.executable
        compiled = True
    else:
        # If the script is being run as a .py file
        script_path = sys.argv[0]
        compiled = False

    if compiled:
        command = script_path
    else:
        command = f'python3 "{script_path}"'

    try:
        if keep_same_console:
            zhmiscellanygsudo.admin_subprocess.run(command)
        else:
            zhmiscellanygsudo.admin_subprocess.Popen(command)
    except Exception as e:
        raise RuntimeError(f"Failed to elevate privileges: {e}")

    # Exit the current script after attempting to rerun as admin
    zhmiscellany.misc.die()


def is_admin():
    return zhmiscellany.misc.is_admin()
