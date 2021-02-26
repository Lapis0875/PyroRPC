from enum import Enum
from typing import Final


class ConfigKeys:
    Version: Final[str] = 'version'
    ClientID: Final[str] = 'client_id'
    Format: Final[str] = 'format'
    Profiles: Final[str] = 'profiles'


class Resources(Enum):
    Campfire = 'campfire'
    Lapis0875 = 'lapis0875'
    Flame1 = 'flame1'
    ReddishFire = 'reddishfire'
    ShrubFire = 'shrubfire'


class ButtonKeys:
    Label: Final[str] = 'label'
    URL: Final[str] = 'url'


class ProfileKeys:
    # Flags
    Enabled: Final[str] = 'enabled'

    # JSON keys
    State: Final[str] = 'state'
    Details: Final[str] = 'details'
    LargeIcon: Final[str] = 'large_icon'
    LargeText: Final[str] = 'large_text'
    SmallIcon: Final[str] = 'small_icon'
    SmallText: Final[str] = 'small_text'
    Buttons: Final[str] = 'buttons'

    # Format constants
    Client: Final[str] = 'client.'

    @staticmethod
    def parseResource(resource_key: str) -> Resources:
        if resource_key.startswith(ProfileKeys.Client):
            key = resource_key.strip(ProfileKeys.Client)
            return next(filter(lambda e: e.name == key, Resources.__members__.values()))
        else:
            raise ValueError('Currently, only resources in client can be used :(')
