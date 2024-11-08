from __future__ import annotations

import mirror
import mirror.toolbox

from pathlib import Path
import json
import time
import logging

class SyncExecuter:
    def __init__(self, package: Package) -> None:
        self.package = package
        self.settings = package.settings
    
    def sync(self) -> None:
        pass

class Worker:
    def __init__(self, package: Package, execute, logger: logging.Logger) -> None:
        self.package = package
        self.logger = logger
        self.sync = SyncExecuter(package)

class Options:
    keys: list[str]
    def __init__(self, inp: dict) -> None:
        self.keys = inp.keys()
        for key in inp:
            if inp[key]:
                setattr(self, key, inp[key])

    def to_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.keys}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

class PackageSettings(Options):
    hidden: bool
    src: str
    dst: str
    options: Options

class Package:
    class Link(Options):
        rel: str
        href: str
    
    class StatusInfo(Options):
        lastsynclog: str
        lastsuccesslog: str
        errorcount: int

    pkgid: str
    name: str
    status: str
    href: str
    synctype: str
    syncrate: int
    link: list[Link]
    settings: PackageSettings

    def __init__(self, config: dict) -> None:
        self.pkgid = config["id"]
        self.name = config["name"]
        self.status = config["status"]
        self.href = config["href"]
        if config["synctype"] in mirror.sync.methods:
            self.synctype = config["synctype"]
        else:
            raise ValueError(f"Sync type not in {mirror.sync.methods}")
        self.syncrate = mirror.toolbox.iso_duration_parser(config["syncrate"])
        self.link = []
        for link in config["link"]:
            self.link.append(self.Link(link))
        self.settings = PackageSettings(config["settings"])
        self.statusinfo = self.StatusInfo(config["statusinfo"])

    def __str__(self) -> str:
        return self.id

    def set_status(self, status) -> None:
        if status == self.status: return
        statuslist = ["ACTIVE", "ERROR", "SYNC", "UNKNOWN"]
        if status not in statuslist:
            raise ValueError(f"Status not in {statuslist}")
        
        self.status = status
        self.timestamp = time.time() * 1000

        if status == "ERROR":
            self.errorcount += 1
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.pkgid,
            "status": self.status,
            "href": self.href,
            "synctype": self.synctype,
            "syncrate": mirror.toolbox.iso_duration_maker(self.syncrate),
            "link": [link.to_dict() for link in self.link],
            "settings": self.settings.to_dict(),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


    def _path_check(self, path: Path) -> None:
        if mirror.debug: return
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")

class Sync:
    pkgid: str
    synctype: str
    logPath: Path | str
    options: Options
    settings: PackageSettings

    def __init__(pkg: Package):
        pkgid = pkg.pkgid
        synctype = pkg.synctype


class Packages(Options):
    def __init__(self, pkgs: dict) -> None:
        self.keys = pkgs.keys()
        for key in pkgs:
            setattr(self, key, Package(pkgs[key]))

    def to_dict(self) -> dict:
        return {key: getattr(self, key).to_dict() for key in self.keys}

class Config:
    class FTPSync(Options):
        maintainer: str
        sponsor: str
        country: str
        location: str
        throughput: str
        include: str
        exclude: str

    name: str
    lastsettingmodified: int

    logfolder: Path
    webroot: Path
    ftpsync: FTPSync

    uid: int
    gid: int

    def __init__(self, config: dict) -> None:
        self.name = config["mirrorname"]

        self._path_check(Path(config["settings"]["logfolder"]))
        self._path_check(Path(config["settings"]["webroot"]))
        self.logfolder = Path(config["settings"]["logfolder"])
        self.webroot = Path(config["settings"]["webroot"])

        self.uid = config["settings"]["uid"]
        self.gid = config["settings"]["gid"]

        self.localtimezone = config["settings"]["localtimezone"]
        self.ftpsync = self.FTPSync(config["settings"]["ftpsync"])
        self.logger = config["settings"]["logger"]
        self.plugins = config["settings"]["plugins"]


    def _path_check(self, path: Path) -> None:
        if mirror.debug: return
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")
        if not path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory")

    def to_dict(self) -> dict:
        return {
            "mirrorname": self.name,
            "settings": {
                "logfolder": self.logfolder,
                "webroot": self.webroot,
                "gid": self.gid,
                "uid": self.uid,
                "localtimezone": self.localtimezone,
                "ftpsync": self.ftpsync.to_dict(),
                "logger": self.logger,
                "plugins": self.plugins,
            }
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    def save(self) -> None:
        mirror.configPath.write_text(self.to_json())

class Packet:
    mode: int
    sender: str
    to: str
    command: str

    def load(self, data: dict) -> None:
        self.mode = data["mode"]
        self.sender = data["sender"]
        self.to = data["to"]
        self.command = data["command"]

        return

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "sender": self.sender,
            "to": self.to,
            "command": self.command,
        }
    
    def to_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(), **kwargs)