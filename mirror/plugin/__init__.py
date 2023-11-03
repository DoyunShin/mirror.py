import mirror

from pathlib import Path
from importlib.machinery import SourceFileLoader

loadable_module = ["sync", "logger", "plugin",]

def plugin_loader():
    """Load the plugins"""
    for plugin in mirror.conf.plugins:
        pluginPath = Path(plugin).resolve()
        if not pluginPath.exists():
            raise FileNotFoundError(f"Plugin {plugin} does not exist!")

        this = SourceFileLoader(f"", str(pluginPath)).load_module()
        check = ["setup", "module", "name", "entry"]
        for attr in check:
            if not hasattr(this, attr):
                raise AttributeError(f"Plugin {plugin} does not have attribute {attr}!")
        
        try:
            if this.module not in loadable_module:
                raise AttributeError(f"Plugin {plugin} does not have a valid module!")
            
            _ = getattr(mirror, this.module) # Check module exists.
            
        except AttributeError:
            raise AttributeError(f"Plugin mirror does not have module {this.module}!")
        
        this = SourceFileLoader(f"mirror.{this.module}.{this.name}", str(pluginPath)).load_module()
        setattr(getattr(mirror, this.module), this.name, this)

        this.setup()

        pass