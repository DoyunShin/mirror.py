import mirror

import os
import time
from pathlib import Path
import subprocess

def rsync(package: mirror.structure.Package):
    """Sync package to mirror"""
    os.setgid(mirror.conf.gid)
    os.setuid(mirror.conf.uid)
    package.setstatus("SYNC")
    logfile = mirror.settings.logdir / f"{package.pkgid}-{time.strftime('%H%M%S')}.log"
    command = [
        "rsync",
        "-vrlptDSH",
        "--exclude=\"*.~tmp~\"",
        "--delete-delay",
        "--delay-updates",
        f'--log-file="{str(logfile)}"'
        f'"{package.settings.src}::{package.settings.path}"',
        f'"{package.settings.dst}"',
    ]

    command = " ".join(command)
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode == 0:
        package.setstatus("ACTIVE")
    else:
        package.setstatus("ERROR")


def ffts(package: mirror.structure.Package):
    """Check if the mirror is up to date"""
    os.setgid(mirror.conf.gid)
    os.setuid(mirror.conf.uid)
    package.setstatus("SYNC")
    command = [ # FFTS Check command
        "rsync",
        "--no-motd",
        "--dry-run",
        "--out-format=\"%n\"",
        f'"{package.settings.src}::{package.settings.path}/{package.settings.fftsfile}"',
        f'"{package.settings.dst}/{package.settings.fftsfile}"',
    ]

    command = " ".join(command)
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.stdout != b'':
        rsync(package) # Not up to date, sync
    else:
        package.setstatus("ACTIVE")
