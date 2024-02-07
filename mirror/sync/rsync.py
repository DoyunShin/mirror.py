import mirror
import mirror.sync
import mirror.logger
import mirror.toolbox
import mirror.structure

import os
import time
import logging
import subprocess

from pathlib import Path

module = "sync"
name = "rsync"
required = ["rsync", "ssh"]
options: dict[str, type] = {
    "ffts": bool,
    "fftsfile": str,
    "auth": bool,
    "userid": str,
    "passwd": str,
}

optionClass = mirror.structure.Options(options)

def setup():
    """
    Setup the plugin
    """
    global required

    for command in required:
        if not mirror.toolbox.is_command_exists(command):
            raise ValueError(f"Command not found: {command}")
    
    return

def execute(package: mirror.structure.Package):
    """
    Run the Sync method (CORE)
    Args:
        package (mirror.structure.Package): Package object
    Returns:
        Null
    """
    if package.status == "SYNC": return

    starttime = time.time()

    logger = mirror.logger.create_logger(f"{module}.{name}", package.pkgid)
    logger.info(f"Staring {module}.{name} for {package.name}")



def rsync(logger: logging.Logger, pkgid: str, src: Path, dst: Path, auth: bool, userid: str, passwd: str):
    """
    Sync Package with rsync

    Args:
        package (mirror.structure.Package): Package object
        logger (logging.Logger): Logger object
    Returns:
        Null
    """
    command = [
        "rsync",
        "-vrlptDSH",
        "--exclude=\"*.~tmp~\"",
        "--delete-delay",
        "--delay-updates",
        f'--log-file="{logger.handlers[1].baseFilename}"',
        f'"{src}"',
        f'"{dst}"',
    ]

    env = os.environ.copy()
    if auth:
        env["USER"] = userid
        env["RSYNC_PASSWORD"] = passwd
    
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, preexec_fn=mirror.sync.setexecuser(mirror.conf.uid, mirror.conf.gid))

    pass
    

def ffts(package: mirror.structure.Package, logger: logging.Logger):
    """Check if the mirror is up to date"""
    logger.info(f"Running FFTS check for {package.name}")
    package.setstatus("SYNC")
    command = [ # FFTS Check command
        "rsync",
        "--no-motd",
        "--dry-run",
        "--out-format=\"%n\"",
        f'"{package.settings.src}::{package.settings.path}/{package.settings.fftsfile}"',
        f'"{package.settings.dst}/{package.settings.fftsfile}"',
    ]

    env = os.environ.copy()
    env["USER"] = package.settings.userid
    env["RSYNC_PASSWORD"] = package.settings.passwd

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, preexec_fn=mirror.sync.setexecuser(mirror.conf.uid, mirror.conf.gid))

    pass
