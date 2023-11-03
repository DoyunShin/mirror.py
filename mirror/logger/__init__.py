import mirror

from prompt_toolkit import PromptSession, print_formatted_text
from pathlib import Path
import logging
import datetime

class PromptHandler(logging.StreamHandler):
    def emit(self, record):
        msg = self.format(record)
        print_formatted_text(msg)


psession = PromptSession()
input = psession.prompt
logger = logging.getLogger("mirror")
basePath: Path = None

logger.handlers = [PromptHandler()]
logger.setLevel(logging.INFO)
logger.handlers[0].setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s # %(message)s"))

def create_logger(package: mirror.structure.Package) -> logging.Logger:
    """Create a logger for a package"""
    logger = logging.getLogger(f"mirror.package.{package.name}")
    formatter = logging.Formatter(mirror.conf.logger["packageformat"].format(package=package.name, packageid=package.pkgid))
    level = logging.getLevelName(mirror.conf.logger["packagelevel"])
    
    prompthandler = PromptHandler()
    prompthandler.setFormatter(formatter)
    prompthandler.setLevel(level)
    logger.handlers = [prompthandler]

    now = datetime.datetime.now()
    folder = basePath / mirror.conf.logger["fileformat"]["folder"].format(year=now.year, month=now.month, day=now.day)
    if not folder.exists():
        folder.mkdir(parents=True)

    filename = folder / mirror.conf.logger["fileformat"]["filename"].format(hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond, packageid=package.pkgid)
    filehandler = logging.FileHandler(filename=str(filename), encoding="utf-8")
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.handlers.append(filehandler)

    if mirror.debug:
        logger.handlers[0].setLevel(logging.DEBUG)
        logger.handlers[1].setLevel(logging.DEBUG)

    return logger

def setup_logger():
    global basePath

    logger = logging.getLogger("mirror")
    logger.setLevel(logging.getLevelName(mirror.conf.logger["level"]))
    formatter = logging.Formatter(mirror.conf.logger["format"])
    logger.handlers[0].setFormatter(formatter)

    basePath = Path(mirror.conf.logger["fileformat"]["base"])
    if not basePath.exists():
        basePath.mkdir(parents=True)
    
    now = datetime.datetime.now()
    folder = basePath / mirror.conf.logger["fileformat"]["folder"].format(year=now.year, month=now.month, day=now.day)
    
    if not folder.exists():
        folder.mkdir(parents=True)
    
    filename = folder / "master.log"
    filehandler = logging.FileHandler(filename=str(filename), encoding="utf-8")
    filehandler.setFormatter(formatter)
    logger.handlers.append(filehandler)

    if mirror.debug:
        logger.setLevel(logging.DEBUG)
        logger.handlers[0].setLevel(logging.DEBUG)
        logger.handlers[1].setLevel(logging.DEBUG)
        