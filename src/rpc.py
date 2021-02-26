from __future__ import annotations
import json
import logging
from time import sleep
from sys import stdout
from typing import Optional, List, Tuple

from pypresence import Presence     # The simple rich presence client in pypresence
from src.script_support import ScriptEngine, ScriptEvent, Script
from src.type_hints import JSON
from src.abstracts import JsonObject, Scriptable
from src.constants import Resources, ButtonKeys, ProfileKeys, ConfigKeys


class Button(JsonObject, Scriptable):
    @classmethod
    def fromJson(cls, data: JSON) -> Button:
        return cls(
            data[ButtonKeys.Label],
            data[ButtonKeys.URL]
        )

    def __init__(
            self,
            label: str,
            url: str
    ) -> None:
        self._label: str = label
        self._url: str = url
        self._script: Optional[Script] = None

    @property
    def label(self) -> str:
        return self._label

    @property
    def url(self) -> str:
        return self._url

    @property
    def script(self) -> Script:
        return self._script

    def setScript(self, script: Script):
        if not isinstance(script, Script):
            raise TypeError('Only Script objects can be set as Button.script')
        self._script = script

    setScript.__doc__ = Scriptable.setScript.__doc__

    def toJson(self) -> JSON:
        return {
            ButtonKeys.Label: self._label,
            ButtonKeys.URL: self._url
        }


class Profile(JsonObject, Scriptable):
    @classmethod
    def fromJson(cls, data: JSON) -> Profile:
        return cls(
            data[ProfileKeys.Enabled],
            data[ProfileKeys.State],
            data[ProfileKeys.Details],
            data.get(ProfileKeys.LargeIcon),
            data.get(ProfileKeys.LargeText),
            data.get(ProfileKeys.SmallIcon),
            data.get(ProfileKeys.SmallText),
            data.get(ProfileKeys.Script)
        )

    def __init__(
            self,
            enabled: bool,
            title: str,
            description: Optional[str] = None,
            large_icon: Optional[str] = None,
            large_text: Optional[str] = None,
            small_icon: Optional[str] = None,
            small_text: Optional[str] = None,
            buttons: Optional[List[JSON]] = None
    ) -> None:
        # Flag
        self._enabled: bool = enabled
        # Info
        self._state: str = title
        self._details: str = '' if description is None else description
        # Resources
        self._largeIcon: Optional[Resources] = None if large_icon is None else ProfileKeys.parseResource(large_icon)
        self._largeText: str = large_text
        self._smallIcon: Optional[Resources] = None if small_icon is None else ProfileKeys.parseResource(small_icon)
        self._smallText: str = small_text
        # Buttons
        buttons = [Button.fromJson(data) for data in buttons]
        if len(buttons) > 2:
            buttons = buttons[:1]
        self._buttons: Tuple[Button] = tuple(buttons)
        self._script: Optional[Script] = None

    @property
    def state(self) -> str:
        return self._state

    @property
    def details(self) -> str:
        return self._details

    @property
    def largeIcon(self) -> Resources:
        return self._largeIcon

    @property
    def largeText(self) -> str:
        return self._largeText

    @property
    def smallIcon(self) -> Resources:
        return self._smallIcon

    @property
    def smallText(self) -> str:
        return self._smallText

    def setScript(self, script: Script):
        if not isinstance(script, Script):
            raise TypeError('Only Script objects can be set as Profile.script')
        self._script = script

    setScript.__doc__ = Scriptable.setScript.__doc__

    def toJson(self) -> JSON:
        return {
            ProfileKeys.Enabled: self._enabled,
            ProfileKeys.State: self._state,
            ProfileKeys.Details: self._details,
            ProfileKeys.LargeIcon: f'{ProfileKeys.Client}{self._largeIcon.name}',
            ProfileKeys.LargeText: self._largeText,
            ProfileKeys.SmallIcon: f'{ProfileKeys.Client}{self._largeIcon.name}',
            ProfileKeys.SmallText: self._smallText,
            ProfileKeys.Buttons: [button.toJson() for button in self._buttons],
            ProfileKeys.Script: self._script.__name__
        }


class LapisRPC:
    def __init__(self, config: JSON) -> None:
        self._config = config
        self._version = config[ConfigKeys.Version]
        self._client_id: int = config[ConfigKeys.ClientID]
        with open('./resources/{}'.format(config[ConfigKeys.Profiles]), mode='rt', encoding='utf-8') as f:
            profiles = json.load(f)
        self._profiles = [Profile.fromJson(profile) for profile in profiles]

        self._client: Presence = Presence(self._client_id)
        self._currentProfile: Optional[Profile] = None
        self._script_engine: ScriptEngine = ScriptEngine(self)
        self.logger = logging.getLogger('pyrorpc')
        self.logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler(stdout)
        consoleHandler.setFormatter(
            logging.Formatter(
                style='{',
                fmt='[{asctime}] [{levelname}] {name} > {message}'
            )
        )
        self.logger.addHandler(consoleHandler)

    @property
    def client_id(self) -> int:
        return self._client_id

    @property
    def version(self) -> str:
        return self._version

    @property
    def profiles(self) -> List[Profile]:
        return self._profiles

    def start(self) -> None:
        self.logger.info('[PyroRPC] Lapis0875@rpc > Starting presence client...')
        self._client.connect()
        self._script_engine.emit(ScriptEvent.OnStart)
        self.logger.info('[PyroRPC] Lapis0875@rpc > Connected!')

    def updateProfile(self, profile: Profile):
        self.logger.info('[PyroRPC] Lapis0875@rpc > Updating presence profile...')
        self._script_engine.emit(ScriptEvent.OnUnload, self._currentProfile)
        self._script_engine.emit(ScriptEvent.OnLoad, profile)
        self._currentProfile = profile
        response = self._client.update(**profile.toJson())
        self.logger.debug(f'{type(response) =}')
        self.logger.debug(f'{response =}')

    def close(self) -> None:
        self.logger.info('[PyroRPC] Lapis0875@rpc > Closing presence client...')
        self._script_engine.emit(ScriptEvent.OnClose)
        self._client.close()
        self.logger.info('[PyroRPC] Lapis0875@rpc > Closed!')
