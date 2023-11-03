import mirror

from pathlib import Path
import json

DEFAULT_CONFIG = {
    "mirrorname": "My Mirror",
    "settings": {
        "logfolder": "/mirror/logs",
        "webroot": "/var/www/mirror",
        "gid": 1000,
        "uid": 1000,
        "localtimezone": "Asia/Seoul",
        "ftpsync": {
            "maintainer": "Admins <admins@examile.com>", # only ftpsync
            "sponsor": "Example <https://example.com>", # only ftpsync
            "country": "KR", # only ftpsync
            "location": "Seoul", # only ftpsync
            "throughput": "1G", # only ftpsync
            "include": "", # only ftpsync
            "exclude": "", # only ftpsync
        },
        "logger": {
            "level": "INFO",
            "packagelevel": "ERROR",
            "format": "[%(asctime)s] %(levelname)s # %(message)s",
            "packageformat": "[%(asctime)s][{package}] %(levelname)s # %(message)s",

            "fileformat": {
                "base": "/mirror/logs",
                "folder": "{year}/{month}/{day}",
                "filename": "{hour}:{minute}:{second}.{microsecond}.{packageid}.log",
                "gzip": True,
            }
        },
        "plugins": [
            "/mirror/plugin/someof.py",
            "/mirror/plugin/"
        ]
    },
    "packages": {
        "mirror": {
            "name": "onTDB Mirror",
            "id": "mirror",
            "href": "/mirror",
            "synctype": "rsync",
            "syncrate": "PT1H",
            "link": [
                {
                    "rel": "HOME",
                    "href": "http://www.ontdb.com"
                },
                {
                    "rel": "HTTP",
                    "href": "http://mirror.ontdb.com/mirror"
                },
                {
                    "rel": "HTTPS",
                    "href": "https://mirror.ontdb.com/mirror"
                }
            ],
            "settings": {
                "hidden": False,
                "src": "rsync://test.org/mirror", # ftp://test.org/mirror
                "dst": "/disk/mirror",
                "options": {
                    "ffts": True,
                    "fftsfile": "fullfiletimelist-mirror", # only FFTS
                }
            }
        }
    }
}

DEF_CONF_PATH = Path("/etc/mirror/config.json")
DEF_DATA_PATH = Path("/etc/mirror/data.json")
DEF_STATUS_PATH = Path("/etc/mirror/status.json")
CONFIG_PATH: Path = None
DATA_PATH: Path = None
STATUS_PATH: Path = None

def load_config(configPath: Path = DEF_CONF_PATH):
    """Load the configuration file"""
    if not configPath.exists():
        raise FileNotFoundError(f"{configPath} does not exist! Please initialize the mirror first.")
    config = json.loads(configPath.read_text())
    if not DEF_DATA_PATH.exists():
        for package in config["packages"]:
            package["status"] = "ERROR"
        DEF_DATA_PATH.write_text(json.dumps(config["packages"]))
    status = json.loads(DEF_DATA_PATH.read_text())

    conflist = list(config["packages"].keys())
    statuslist = list(status["packages"].keys())
    for package in conflist:
        if package in statuslist:
            config["packages"][package]["status"] = status["packages"][package]["status"]
            statuslist.remove(package)
        else:
            config["packages"][package]["status"] = "ERROR"
    
    if statuslist:
        mirror.logger.warning(f"Status file has extra packages: {statuslist}. You might need to delete manually.")
    
    DEF_DATA_PATH.write_text(json.dumps(config))
    




    mirror.settings = mirror.config.Settings(config)
    
def reload():
    config = json.loads(CONFIG_PATH.read_text())
   