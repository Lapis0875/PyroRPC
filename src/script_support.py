from __future__ import annotations

from enum import Enum
from typing import List, Optional, Any


class Script:
    def __init__(self, client) -> None:
        self._client = client

    def onLoad(self) -> None:
        pass

    def onCalled(self, *args, **kwargs) -> None:
        pass

    def onUnload(self) -> None:
        pass

    # Alias support
    @classmethod
    def register(cls, script_cls: type) -> type:
        return ScriptEngine.register(script_cls)


class ScriptEvent(Enum):
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
