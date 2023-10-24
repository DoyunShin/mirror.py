synctypes = ["ffts", "rsync", "ftp", "ftpsync", "bandersnatch"]


import mirror.event
import mirror.structure
import mirror.sync
import mirror.logger
import mirror.command
import mirror.socket
import mirror.config

from pathlib import Path
import logging

conf: mirror.structure.Config
confPath: Path
publishPath: Path
