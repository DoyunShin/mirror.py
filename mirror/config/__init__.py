import mirror

from pathlib import Path
import json

DEFAULT_CONFIG = {
    "lastsettingmodified": "",
    "mirrorname": "My Mirror",
    "settings": {
        "logfolder": "/mirror/logs",
        "webroot": "/var/www/mirror",
        "gid": 1000,
        "uid": 1000,
        "ftpsync": {
            "maintainer": "Admins <admins@examile.com>", # only ftpsync
            "sponsor": "Example <https://example.com>", # only ftpsync
            "country": "KR", # only ftpsync
            "location": "Seoul", # only ftpsync
            "throughput": "1G", # only ftpsync
            "include": "", # only ftpsync
            "exclude": "", # only ftpsync
        }
    },
    "packages": {
        "mirror": {
            "name": "onTDB Mirror",
            "id": "mirror",
            "status": "ACTIVE",
            "href": "/mirror",
            "synctype": "FFTS",
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
                "type": "FFTS",
                "src": "test.org",
                "srcpath": "mirror", # test.org/mirror
                "dst": "/disk/mirror",
                "additional": {
                    "ffts": True,
                    "fftsfile": "fullfiletimelist-mirror", # only FFTS
                }
            }
        }
    }
}

def load_config(configPath: Path):
    """Load the configuration file"""
    config = json.loads(configPath.read_text())
    mirror.settings = mirror.config.Settings(config)
    

