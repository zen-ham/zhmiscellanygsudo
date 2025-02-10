import psutil, sys, subprocess, base64, pickle, time
args = sys.argv
args.pop(0)


def decode_and_unpickle(encoded_str):
    """Decodes a URL-safe encoded string and unpickles the object."""
    pickled_data = base64.urlsafe_b64decode(encoded_str)  # Decode from Base64
    obj = pickle.loads(pickled_data)  # Deserialize
    return obj


execution_pid = int(args[0])
command_data = args[1]
command = decode_and_unpickle(command_data)

proc = subprocess.Popen(command)
try:
    while psutil.pid_exists(execution_pid) and proc.poll() is None:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
try:
    proc.kill()
except:
    pass