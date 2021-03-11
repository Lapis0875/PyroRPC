from __future__ import annotations

import inspect
from enum import Enum
from os.path import sep
from pprint import pprint
from typing import List, Optional, Any, Union, Dict, Callable


class Script:
    def __init__(self, client) -> None:
        self._client = client
        self._name = self.__class__.__name__

    @property
    def client(self):
        """

        Returns:
             src.rpc.LapisRPC object.
        """
        return self._client

    @property
    def name(self) -> str:
        return self._name

    def onStart(self) -> None:
        """An event called when RPC client has been started."""
        pass

    def onClose(self) -> None:
        """An event called when RPC client has been closed."""
        pass

    def onLoad(self, profile) -> None:
        """
        An event called when Script is loaded.

        Args:
            profile (src.discordrpc.Profile) : Profile object which is loaded.
        """
        pass

    def onUnload(self, profile) -> None:
        """
        An event called when Script is unloaded.

        Args:
            profile (src.discordrpc.Profile) : Profile object which is unloaded.
        """
        pass

    def onReload(self, profile) -> None:
        """
        An event called when Script is reloaded.

        Args:
            profile (src.discordrpc.Profile) : Profile object which is unloaded.
        """
        pass

    def onUpdate(self, profile, **attrs) -> None:
        """
        An event called when Script is updated.

        Args:
            profile (src.discordrpc.Profile) : Profile object which is updated.
            **attrs (Any) : Updated profile attributes.
        """

    def onClick(self, profile, button) -> None:
        """
        An event called when button on rpc profile is clicked.

        Args:
            profile (src.discordrpc.Profile) : Profile object
            button (src.discordrpc.Button) : Button object which is clicked by someone.
        """
        pass

    # Alias support
    @classmethod
    def register(cls, script_cls: type) -> type:
        return ScriptEngine.register(script_cls)

# Remains of attempt to create ScriptEvent enumeration with `doc` attribute from function.__doc__
# class EventEnumMeta(EnumMeta):
#     def __new__(mcs, name, bases, attrs):
#         obj = super().__new__(mcs, name, bases, attrs)
#         obj._value2member_map_ = {}
#         for m in obj:
#             name, doc = m.value
#             m._value_ = name
#             m.doc = doc
#             obj._value2member_map_[name] = m
#
#         return obj


class ScriptEventWrapper:
    mock: Callable[..., None]
    name: str
    doc: str

    def __init__(self, func):
        self.mock = func    # Save mock function object
        self.name = func.__name__
        self.doc = inspect.cleandoc(func.__doc__)


class ScriptEvent(Enum):
    OnStart = ScriptEventWrapper(Script.onStart)
    OnClose = ScriptEventWrapper(Script.onClose)
    OnLoad = ScriptEventWrapper(Script.onLoad)
    OnUnload = ScriptEventWrapper(Script.onUnload)
    OnReload = ScriptEventWrapper(Script.onReload)
    OnUpdate = ScriptEventWrapper(Script.onUpdate)
    OnClick = ScriptEventWrapper(Script.onClick)

    @property
    def eventName(self) -> str:
        return self.value.name

    @property
    def doc(self) -> str:
        return self.value.doc

    # Remains of attempt to create ScriptEvent enumeration with `doc` attribute from function.__doc__
    # OnStart = Script.onStart
    # OnClose = Script.onClose
    # OnLoad = Script.onLoad
    # OnUnload = Script.onUnload
    # OnReload = Script.onReload
    # OnUpdate = Script.onUpdate
    # OnClick = Script.onClick


class ScriptEngine:
    @classmethod
    def register(cls, script_cls: type, filename: str = None) -> type:
        if filename is None:
            outerFrame = inspect.getouterframes(inspect.currentframe())[1]
            filename = outerFrame.filename.split(sep)[-1].replace('.py', '')
            print(filename)
        if not issubclass(script_cls, Script):
            raise TypeError('Only subclass of Script can be registered!')

        print(f'Registering new script class {script_cls}')
        scripts = getattr(cls, '__scripts__', None)
        if scripts is None:
            scripts = {}
            setattr(cls, '__scripts__', scripts)

        fileScripts = scripts.get(filename)
        if fileScripts is None:
            scripts[filename] = fileScripts = {}
        fileScripts[script_cls.__name__] = script_cls

        return script_cls

    def __init__(self, client, module):
        """
        Initialize ScriptEngine.
        Args:
            client (src.discordrpc.DiscordRPC) : RPC client to register scripts.
            module : Python module object referencing 'scripts/' module.
        """
        print('Initializing ScriptEngine')
        self._client = client
        self._module = module
        registeredScripts = getattr(self.__class__, '__scripts__', None)
        pprint(registeredScripts, indent=4)
        self._scriptsMap: Dict[str, Dict[str, Script]] = {}        # filename: {classname: cls, classname: cls, ...}
        if registeredScripts is not None:
            for filename, scripts in registeredScripts.items():
                self._scriptsMap[filename] = {}
                for scriptName, script in scripts.items():
                    self._scriptsMap[filename][scriptName] = script(client)
        self._scriptsList: List[Script] = []
        for scripts in self._scriptsMap.values():
            for script in scripts.values():
                self._scriptsList.append(script)
        print('scripts list :')
        pprint(self._scriptsList)
        print('Collecting script event listeners...')
        self._eventMap: Dict[ScriptEvent, List[Callable[..., Any]]] = {}
        for event in ScriptEvent.__members__.values():
            print(f'Collecting listeners of event {event.eventName}')
            print(event)
            for script in self._scriptsList:
                callback = getattr(script, event.eventName, None)
                if callback is not None:
                    try:
                        self._eventMap[event].append(callback)
                    except KeyError:
                        self._eventMap[event] = [callback]
        print('Collected event listener map : ')
        pprint(self._eventMap, indent=4)

    @property
    def client(self):
        return self._client

    @property
    def module(self):
        return self._module

    def emit(self, event: ScriptEvent, *args, **kwargs):
        for callback in self._eventMap[event]:
            callback(*args, **kwargs)

    def getScript(self, fileName: str, scriptName: str) -> Optional[Script]:
        print(f'{fileName=},{scriptName=}')
        pprint(f'{self._scriptsMap=}')
        result = tuple(filter(lambda script: script.name == scriptName, self._scriptsMap[fileName].values()))
        pprint(result)
        try:
            return result[0]
        except IndexError:
            return None
