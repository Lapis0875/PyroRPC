from __future__ import annotations
import json
import logging
from time import sleep
from sys import stdout
from typing import Optional, List, Tuple

from pypresence import Presence     # The simple rich presence client in pypresence
import psutil

from src.script_support import ScriptEngine, ScriptEvent
from src.type_hints import JSON
from src.abstracts import JsonObject
from src.constants import Resources, ButtonKeys, ProfileKeys, ConfigKeys


class Button(JsonObject):
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
        self._label = label
        self._url = url

    @property
    def label(self) -> str:
        return self._label

    @property
    def url(self) -> str:
        return self._url

    def toJson(self) -> JSON:
        return {
            ButtonKeys.Label: self._label,
            ButtonKeys.URL: self._url
        }

class Profile(JsonObject):
    @classmethod
    def fromJson(cls, data: JSON) -> Profile:
        return cls(
            data[ProfileKeys.Enabled],
            data[ProfileKeys.State],
            data[ProfileKeys.Details],
            data.get('large_icon'),
            data.get('large_text'),
            data.get('small_icon'),
            data.get('small_text')
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
        self._large_icon: Optional[Resources] = None if large_icon is None else ProfileKeys.parseResource(large_icon)
        self._large_text: str = large_text
        self._small_icon: Optional[Resources] = None if small_icon is None else ProfileKeys.parseResource(small_icon)
        self._small_text: str = small_text
        # Buttons
        buttons = [Button.fromJson(data) for data in buttons]
        if len(buttons) > 2:
            buttons = buttons[:1]
        self._buttons: Tuple[Button] = tuple(buttons)

    @property
    def state(self) -> str:
        return self._state

    @property
    def details(self) -> str:
        return self._details

    def toJson(self) -> JSON:
        return {
            ProfileKeys.Enabled: self._enabled,
            ProfileKeys.State: self._state,
            ProfileKeys.Details: self._details,
            ProfileKeys.LargeIcon: f'{ProfileKeys.Client}{self._large_icon.name}',
            ProfileKeys.LargeText: self._large_text,
            ProfileKeys.SmallIcon: f'{ProfileKeys.Client}{self._large_icon.name}',
            ProfileKeys.SmallText: self._small_text,
            ProfileKeys.Buttons: [button.toJson() for button in self._buttons]
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
        self._script_engine: ScriptEngine = ScriptEngine(self)
        self.logger = logging.getLogger('rpc.lapis0875')
        self.logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler(stdout)
        consoleHandler.setFormatter(
            logging.Formatter(
                style='{',
                fmt=''
            )
        )
        self.logger.addHandler(

        )

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
        self._client.connect()
        self._script_engine.emit(ScriptEvent.OnLoad)

    def updateProfile(self, profile: Profile):
        response = self._client.update(**profile.toJson())


def init():
    print('Initialize PyroRPC[Test]')
    RPC = Presence('')    # Initialize the Presence client
    RPC.connect()   # Start the handshake loop
    return RPC


def loop(RPC: Presence):
    print('Loop PyroRPC[Test]')
    while True:
        RPC.update(
            state='Studying...',
            details='2022 EBS 수능특강 영어',
            large_image=Resources.Lapis0875.value,
            large_text='Lapis0875',
            small_image=Resources.Flame1.value,
            small_text='Studying English'
        )  # Updates our presence
        sleep(15)


def main():
    print('Start PyroRPC[Test]')
    RPC = init()
    loop(RPC)
    print('Stop PyroRPC[Test]')


if __name__ == '__main__':
    main()
