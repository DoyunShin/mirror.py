import mirror
import mirror.toolbox

from pathlib import Path
import json
import time
import re

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

class Package:
    class InSettings(Options):
        hidden: bool
        src: str
        dst: str

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
    settings: InSettings

    def __init__(self, config: dict) -> None:
        self.pkgid = config["id"]
        self.name = config["name"]
        self.status = config["status"]
        self.href = config["href"]
        if config["synctype"] in mirror.sync.methods:
            self.synctype = config["synctype"]
        else:
            raise ValueError(f"Sync type not in {mirror.sync.methods}")
        self.syncrate = mirror.toolbox.iso8601_parser(config["syncrate"])
        self.link = []
        for link in config["link"]:
            self.link.append(self.Link(link))
        self.settings = self.InSettings(config["settings"])
        #self.original = config

    def __str__(self) -> str:
        return self.id

    def set_status(self, status) -> None:
        if status == self.status: return
        statuslist = ["ACTIVE", "ERROR", "SYNC", "UNKNOWN"]
        if status in statuslist:
            self.status = status
            self.timestamp = time.time() * 1000
        else:
            raise ValueError(f"Status not in {statuslist}")
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.pkgid,
            "status": self.status,
            "href": self.href,
            "synctype": self.synctype,
            "syncrate": mirror.toolbox.iso8601_maker(self.syncrate),
            "link": [link.to_dict() for link in self.link],
            "settings": self.settings.to_dict(),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


    def _path_check(self, path: Path) -> None:
        if mirror.debug: return
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")

class Config:
    class InPackage(Options):
        def __init__(self, packages: dict) -> None:
            for key in packages:
                setattr(self, key, Package(packages[key]))
            pass

        def to_dict(self) -> dict:
            return {key: getattr(self, key).to_dict() for key in self.keys}

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
    packages: InPackage

    logfolder: Path
    webroot: Path
    ftpsync: FTPSync

    uid: int
    gid: int

    def __init__(self, config: dict) -> None:
        self.name = config["mirrorname"]
        self.packages = self.InPackage(config["packages"])

        self._path_check(Path(config["settings"]["logfolder"]))
        self._path_check(Path(config["settings"]["webroot"]))
        self.logfolder = Path(config["settings"]["logfolder"])
        self.webroot = Path(config["settings"]["webroot"])
        self.ftpsync = self.FTPSync(config["settings"]["ftpsync"])

        self.uid = config["settings"]["uid"]
        self.gid = config["settings"]["gid"]

    def _path_check(self, path: Path) -> None:
        if mirror.debug: return
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")
        if not path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory")

    def to_dict(self) -> dict:
        return {
            "mirrorname": self.name,
            "lastsettingmodified": self.lastsettingmodified,
            "packages": self.packages.to_dict(),
            "settings": {
                "logfolder": self.logfolder,
                "webroot": self.webroot,
                "gid": self.gid,
                "uid": self.uid,
                "ftpsync": self.ftpsync.to_dict(),
            }
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    def save(self) -> None:
        mirror.configPath.write_text(self.to_json())