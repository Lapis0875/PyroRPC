from __future__ import annotations

from enum import Enum
from typing import List, Optional, Any


class Script:
    def __init__(self, client) -> None:
        self._client = client

    def onStart(self) -> None:
        """An event called when RPC client has been started."""
        pass

    def onClose(self) -> None:
        """An event called when RPC client has been closed."""
        pass

    def onLoad(self, profile) -> None:
        """
        An event called when Script is loaded.

        """
        pass

    def onUnload(self) -> None:
        """An event called when Script is unloaded."""
        pass

    # Alias support
    @classmethod
    def register(cls, script_cls: type) -> type:
        return ScriptEngine.register(script_cls)


class ScriptEvent(Enum):
    OnStart = Script.onStart.__name__
    OnClose = Script.onClose.__name__
    OnLoad = Script.onLoad.__name__
    OnUnload = Script.onUnload.__name__


class ScriptEngine:
    @classmethod
    def register(cls, script_cls: type) -> type:
        if not issubclass(script_cls, cls):
            raise TypeError('Only subclass of ')

        scripts = getattr(cls, '__scripts__', None)
        if scripts is None:
            scripts = []
            setattr(cls, '__scripts__', scripts)
        scripts.append(script_cls)

        return script_cls

    def __init__(self, client):
        """
        Initialize ScriptEngine.
        Args:
            client (src.rpc.LapisRPC) : RPC client to register scripts.
        """
        self._client = client
        self._scripts: List[Script] = [s(client) for s in getattr(ScriptEngine, '__scripts__', [])]

    def emit(self, event: ScriptEvent, *args, **kwargs):
        for script in self._scripts:
            callback = getattr(script, event.value, None)
            if callback is not None:
                callback(*args, **kwargs)
