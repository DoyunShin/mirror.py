import mirror.toolbox
import mirror.event
import mirror.sync
import mirror.structure
import mirror.logger
import mirror.command
import mirror.socket
import mirror.config

from pathlib import Path
import logging

conf: mirror.structure.Config
packages: mirror.structure.Packages
confPath: Path
publishPath: Path
logger: logging.Logger
debug: bool

mirror.sync.load_default()
