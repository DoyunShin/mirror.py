import mirror

from importlib.machinery import SourceFileLoader
from pathlib import Path

BasicMethodPath = Path(__file__).parent
methods = [method.stem for method in BasicMethodPath.glob("*.py") if method.stem != "__init__"]
now = []

def loader(methodPath: Path) -> None:
    """Load the sync moodules"""
    methodsFullPath = [method for method in methodPath.glob("*.py") if method.stem != "__init__"]
    for method in methodsFullPath:
        this = SourceFileLoader(f"mirror.sync.{method.stem}", str(method)).load_module()
        setattr(mirror.sync, method.stem, this)

def load_default():
    """Load the default sync moodules"""
    loader(BasicMethodPath)
