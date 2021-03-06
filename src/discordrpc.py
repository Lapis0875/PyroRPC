from __future__ import annotations

import importlib
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
            data.get(ProfileKeys.Buttons),
            data.get(ProfileKeys.Script)
        )

    def __init__(
            self,
            enabled: bool,
            description: Optional[str] = None,
            state: Optional[str] = None,
            large_icon: Optional[str] = None,
            large_text: Optional[str] = None,
            small_icon: Optional[str] = None,
            small_text: Optional[str] = None,
            buttons: Optional[List[JSON]] = None,
            scriptName: Optional[str] = None
    ) -> None:
        # Flag
        self._enabled: bool = enabled
        # Info
        self._details: str = '' if description is None else description
        self._state: str = state
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
        self._scriptInfo: Tuple[str, ...] = tuple(scriptName.split('.'))
        self._script: Optional[Script] = None

    @property
    def details(self) -> str:
        return self._details

    @details.setter
    def details(self, new: str):
        if not isinstance(new, str):
            raise TypeError('Profile.details must be a str object!')
        self._details = new

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, new: str):
        if not isinstance(new, str):
            raise TypeError('Profile.state must be a str object!')
        self._state = new

    @property
    def largeIcon(self) -> Resources:
        return self._largeIcon

    @largeIcon.setter
    def largeIcon(self, new: Resources):
        if not isinstance(new, Resources):
            raise TypeError('Profile.largeIcon must be a Resources enum!')
        self._largeIcon = new

    @property
    def largeText(self) -> str:
        return self._largeText

    @largeText.setter
    def largeText(self, new: str):
        if not isinstance(new, str):
            raise TypeError('Profile.largeText must be a str object!')
        self._largeText = new

    @property
    def smallIcon(self) -> Resources:
        return self._smallIcon

    @smallIcon.setter
    def smallIcon(self, new: Resources):
        if not isinstance(new, Resources):
            raise TypeError('Profile.smallIcon must be a Resources enum!')
        self._smallIcon = new

    @property
    def smallText(self) -> str:
        return self._smallText

    @smallText.setter
    def smallText(self, new: str):
        if not isinstance(new, str):
            raise TypeError('Profile.smallText must be a str object!')
        self._smallText = new

    @property
    def scriptInfo(self) -> Tuple[str, str]:
        return self._scriptInfo

    def setScript(self, script: Script):
        if not isinstance(script, Script):
            raise TypeError('Only Script objects can be set as Profile.script')
        self._script = script

    setScript.__doc__ = Scriptable.setScript.__doc__

    def loadScript(self):
        importlib.import_module(f'scripts.{".".join(self._scriptInfo)}')

    def toJson(self) -> JSON:
        return {
            ProfileKeys.State: self._state,
            ProfileKeys.Details: self._details,
            ProfileKeys.LargeIcon: self._largeIcon.value,
            ProfileKeys.LargeText: self._largeText,
            ProfileKeys.SmallIcon: self._smallIcon.value,
            ProfileKeys.SmallText: self._smallText,
            ProfileKeys.Buttons: [button.toJson() for button in self._buttons]
        }


class DiscordRPC:
    def __init__(self, config: JSON) -> None:
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
        self._config = config
        self._version = config[ConfigKeys.Version]
        self._client_id: int = config[ConfigKeys.ClientID]
        self._client: Presence = Presence(self._client_id)
        scriptModule = importlib.import_module('scripts')
        self._scriptEngine: ScriptEngine = ScriptEngine(self)

        with open('./resources/{}'.format(config[ConfigKeys.Profiles]), mode='rt', encoding='utf-8') as f:
            profiles = json.load(f)
        self._profileFormat: str = profiles[ConfigKeys.Format]
        # self._profiles = [Profile.fromJson(profile) for profile in profiles[ConfigKeys.Data]]
        self._profiles = list(
            map(
                lambda p: Profile.fromJson(p),
                profiles[ConfigKeys.Data]
            )
        )
        for profile in self._profiles:
            script = self._scriptEngine.getScript(*profile.scriptInfo)
            if script is not None:
                profile.setScript(script)
        self._currentProfile: Optional[Profile] = None

    @property
    def client_id(self) -> int:
        return self._client_id

    @property
    def version(self) -> str:
        return self._version

    @property
    def profiles(self) -> List[Profile]:
        return self._profiles

    @property
    def scriptEngine(self) -> ScriptEngine:
        return self._scriptEngine

    def start(self) -> None:
        self.logger.info('Starting presence client...')
        self._client.connect()
        self._scriptEngine.emit(ScriptEvent.OnStart)
        if self._currentProfile is None:
            self.updateProfile(self._profiles[0])
        self.logger.info('Lapis0875@rpc > Connected!')

    def updateProfile(self, profile: Profile):
        self.logger.info('Updating presence profile...')
        if profile == self._currentProfile:
            response = self._client.update(**profile.toJson())
            self.logger.debug(f'{type(response) =}')
            self.logger.debug(f'{response =}')
            return

        if self._currentProfile is not None:
            self._scriptEngine.emit(ScriptEvent.OnUnload, self._currentProfile)
        self._scriptEngine.emit(ScriptEvent.OnLoad, profile)
        self._currentProfile = profile
        response = self._client.update(**profile.toJson())
        self.logger.debug(f'{type(response) =}')
        self.logger.debug(f'{response =}')

    def reloadProfile(self):
        self.logger.info('Reloading presence profile...')
        self._scriptEngine.emit(ScriptEvent.OnReload, self._currentProfile)
        response = self._client.update(**self._currentProfile.toJson())

    def loop(self):
        while True:
            # Temporary loop.
            self.reloadProfile()
            sleep(15)

    def close(self) -> None:
        self.logger.info('Closing presence client...')
        self._scriptEngine.emit(ScriptEvent.OnClose)
        self._client.close()
        self.logger.info('Closed!')
