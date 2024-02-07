import mirror

import threading
import types

events = []

class BasicEvent():
    pre_listeners: list
    post_listeners: list
    threads: list

    def __init__(self):
        self.listeners = []
        pass

    def _call(self, listeners: list[types.FunctionType], *args, **kwargs):
        for listener in listeners:
            _this = threading.Thread(target=listener, args=args, kwargs=kwargs, daemon=True)
            _this.start()
            self.threads.append(_this)

    def add_listener(self, listener: types.FunctionType, pre: bool = False):
        if pre:
            self.pre_listeners.append(listener)
        else:
            self.post_listeners.append(listener)

    def remove_listener(self, listener: types.FunctionType, pre: bool = False):
        if pre:
            self.pre_listeners.remove(listener)
        else:
            self.post_listeners.remove(listener)
    
    def wait(self):
        for thread in self.threads:
            thread.join()
        self.threads = []
    
