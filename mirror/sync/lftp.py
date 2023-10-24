import mirror

import os
import subprocess

def ftp(package: mirror.structure.Package):
    """Sync package to mirror"""
    os.setgid(mirror.conf.gid)
    os.setuid(mirror.conf.uid)

    command = [
        "lftp",
        "-c",
        f'"set ftp:anon-pass mirror@{package.settings.src}; set cmd:verbose yes; set list-options -a mirror --continue --delete --no-perms --verbose=3 -X \'\\.(mirror|notar)\' -x \'\\.in\\..*\\.\/ -X \'lost+found\' '
    ]
    