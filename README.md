`zhmiscellanygsudo`,
===


An extremely useful and unique fully-featured wrapper of [gsudo](https://github.com/gerardog/gsudo) for python.
---

[Introduction](https://github.com/zen-ham/zhmiscellanygsudo/tree/master#Introduction) \
[Usage examples](https://github.com/zen-ham/zhmiscellanygsudo/tree/master#Usage-examples) \
[Documentation](https://github.com/zen-ham/zhmiscellanygsudo/tree/master#Documentation)

---

Introduction
===

This package was made to *once and for all* solve common issue of rerunning python scripts and pyinstaller binaries as admin, and so much more! even able to execute processes as SYSTEM or even TrustedInstaller! (SYSTEM is higher then admin, and TrustedInstaller is the highest privilege level on Windows machines!)

Take this example; if I have a script prints some useful info, that happens to need to be run as admin whenever it's called, but I don't want to always call it from an admin shell. The only way to solve this before was to run the script in as admin in a new window, but now all my useful information that our imaginary script just printed out is all in that new window! What to do? Well, by default on Windows, it is actually *impossible* to run a process as admin and keep its console output inside the same window. But not anymore! With functions such as `zhmiscellanygsudo.admin_subprocess.Popen()` we can all have the best of both worlds!

Supports use with pyinstaller and other python packagers!

Can be installed with `pip install zhmiscellanygsudo`

The git repository for this package can be found [here](https://github.com/zen-ham/zhmiscellanygsudo). The docs also look nicer on github.

If you want to reach out, you may add me on discord at @z_h_ or join [my server](https://discord.gg/ThBBAuueVJ).


Usage examples
===
---

Re-running as admin and retaining console window:

```py
import zhmiscellanygsudo
# Are we admin? Lets find out.
print(zhmiscellanygsudo.is_admin())
# If we're not, this script/executable will be re ran as admin, all the while retaining the same console window, as if by magic!
zhmiscellanygsudo.rerun_as_admin(keep_same_console=True)  # keeping the same console window is default behavior if not specified
# we can be confident that we will only get to this line once the script is running with admin.
print("Hey, I'm running as admin now!")
```
---

Running another script with the highest possible privileges:

```py
import zhmiscellanygsudo
zhmiscellanygsudo.admin_subprocess.run('python another_script.py', run_as_TrustedInstaller=True)  # the same high privilege arguments are available for the rerun function too
```




Documentation:
===
---
`zhmiscellanygsudo.rerun_as_admin()`
---

`zhmiscellanygsudo.rerun_as_admin(run_as_SYSTEM=False, run_as_TrustedInstaller=False, keep_same_console=True)`

By default, rerun the current script as admin. Optionally run as SYSTEM or even TrustedInstaller.

#

`zhmiscellanygsudo.admin_subprocess.Popen()`
---

`zhmiscellanygsudo.admin_subprocess.Popen(command, run_as_SYSTEM=False, run_as_TrustedInstaller=False, **kwargs)`

Works the exact same way as the beloved subprocess.Popen, but by default run the command as admin. Returns a subprocess "process" object, again, exactly the same as subprocess. Optionally run as SYSTEM or even TrustedInstaller.

#

`zhmiscellanygsudo.admin_subprocess.run()`
---

`zhmiscellanygsudo.admin_subprocess.run(command, run_as_SYSTEM=False, run_as_TrustedInstaller=False, **kwargs)`

Works the exact same way as subprocess.run, but by default run the command as admin. Returns a subprocess "process" object, again, exactly the same as subprocess. Optionally run as SYSTEM or even TrustedInstaller.

#

`zhmiscellanygsudo.is_admin()`
---

`zhmiscellanygsudo.is_admin(simple=False)`

Returns strings `Normal` if the current process isn't running as admin, returns `Admin` if the process is running with admin, returns `SYSTEM` if the process is running as SYSTEM, and returns `TrustedInstaller` if running as TrustedInstaller. On some machines it may return an incorrect result when running as SYSTEM or TrustedInstaller, but only inaccurate between those 2 selections.

if `simple` is set to True, then it will return False if not running with admin privileges or above, and True if it is.
#
