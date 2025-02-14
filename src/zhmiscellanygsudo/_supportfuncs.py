import os, zhmiscellany, sys, ctypes, subprocess, win32security, win32api


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
    
    from ._resource_files_lookup import resource_files_lookup
    for file in resource_files_lookup:
        if not os.path.exists(os.path.join(base_path, file)):
            anyway = True  # missing file detected
            break
    
    cwd = os.getcwd()
    if (not os.path.exists(os.path.join(base_path, 'resources'))) or anyway:
        os.chdir(base_path)
        from ._py_resources import gen
        gen()
        os.chdir(cwd)
    return os.path.join(base_path, 'resources', 'x64', 'gsudo.exe')


_gsudo_binary_path = get_gsudo_binary_path()


def rerun_as_admin(run_as_SYSTEM=False, run_as_TrustedInstaller=False):
    requested_level = 1
    if run_as_SYSTEM:
        requested_level = 2
    if run_as_TrustedInstaller:
        requested_level = 3

    current_level = is_admin()

    if current_level >= requested_level:  # if the process is already running at or above the requested privilege level then don't do anything
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
        command = [script_path]
    else:
        command = ['python', script_path]
    command.extend(sys.argv[1:])
    
    command_data = zhmiscellany.fileio.pickle_and_encode(command)
    
    exec_term_handler = os.path.join(os.path.dirname(_gsudo_binary_path), 'execution_termination_handler.exe')
    
    command = [exec_term_handler, str(os.getpid()), command_data]
    
    try:
        process = Popen(command, run_as_SYSTEM=run_as_SYSTEM, run_as_TrustedInstaller=run_as_TrustedInstaller)
        try:
            process.wait()
        except:
            pass
    except Exception as e:
        raise RuntimeError(f"Failed to elevate privileges: {e}"+f'\ncurrent_level {current_level}\nrequested_level {requested_level}')

    failed = process.returncode == 999

    # Exit the current script after attempting to rerun as admin
    if not failed:
        zhmiscellany.misc.die()
    else:
        raise RuntimeError(f"Failed to elevate privileges, operation was canceled by the user."+f'\ncurrent_level {current_level}\nrequested_level {requested_level}')


def is_admin(simple=False):
    # Get the current process token
    process_token = win32security.OpenProcessToken(
        win32api.GetCurrentProcess(),
        win32security.TOKEN_QUERY
    )

    # Get the user SID
    user_sid, _ = win32security.GetTokenInformation(
        process_token, win32security.TokenUser
    )

    # Lookup the account name and domain
    account_name, domain_name, account_type = win32security.LookupAccountSid(None, user_sid)

    # Check if the account is part of the Administrators group
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()

    # Determine the privilege level
    if account_name == 'SYSTEM':
        privilege_level = 2
    elif account_name == 'TrustedInstaller':
        privilege_level = 3
    elif is_admin:
        privilege_level = 1
    else:
        privilege_level = 0

    # extra check to make sure
    if privilege_level == 2:
        result = subprocess.run(['whoami', '/priv'], capture_output=True, text=True)
        if len(result.stdout) > 2754:
            privilege_level = 3

    return privilege_level


def run(command, run_as_SYSTEM=False, run_as_TrustedInstaller=False, **kwargs):
    inserted_command = f'{_gsudo_binary_path}{" -s" if run_as_SYSTEM and not run_as_TrustedInstaller else ""}{" --ti" if run_as_TrustedInstaller else ""}'
    if type(command) == list:
        command.insert(0, inserted_command)
    elif type(command) == str:
        command = f'{inserted_command} {command}'
    else:
        raise TypeError(f'Invalid command type "{type(command)}" for zhmiscellanygsudo.run, requires list or str')
    process = subprocess.run(command, **kwargs)
    return process


def Popen(command, run_as_SYSTEM=False, run_as_TrustedInstaller=False, **kwargs):
    inserted_command = f'{_gsudo_binary_path}{" -s" if run_as_SYSTEM and not run_as_TrustedInstaller else ""}{" --ti" if run_as_TrustedInstaller else ""}'
    if type(command) == list:
        command.insert(0, inserted_command)
    elif type(command) == str:
        command = f'{inserted_command} {command}'
    else:
        raise TypeError(f'Invalid command type "{type(command)}" for zhmiscellanygsudo.Popen, requires list or str')
    process = subprocess.Popen(command, **kwargs)
    return process
