import mirror

from prompt_toolkit import PromptSession, print_formatted_text
import logging

class PromptHandler(logging.StreamHandler):
    def emit(self, record):
        msg = self.format(record)
        print_formatted_text(msg)


psession = PromptSession()
input = psession.prompt
logger = logging.getLogger("mirror")

logger.handlers = [PromptHandler()]
logger.setLevel(logging.INFO)
logger.handlers[0].setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s # %(message)s"))

def create_logger(package: mirror.structure.Package) -> logging.Logger:
    """Create a logger for a package"""
    logger = logging.getLogger(f"mirror.package.{package.name}")
    logger.handlers = [PromptHandler()]
    logger.setLevel(logging.INFO)
    logger.handlers[0].setFormatter(logging.Formatter(f"[%(asctime)s] %(levelname)s # %(package) # %(message)s"))

    return logger