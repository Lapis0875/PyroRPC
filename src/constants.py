from enum import Enum
from typing import Final


class ConfigKeys:
    # config.json
    Version: Final[str] = 'version'
    ClientID: Final[str] = 'client_id'
    Profiles: Final[str] = 'profiles'
    # profiles.json
    Format: Final[str] = 'format'
    Data: Final[str] = 'data'


class Resources(Enum):
    Campfire = 'campfire'
    Profile = 'profile'
    Default = 'default'
    Study = 'study'
    Cafe = 'cafe'
    Game = 'game'
    AFK = 'afk'
    AwayFromKeyboard = AFK  # Alias


class ButtonKeys:
    Label: Final[str] = 'label'
    URL: Final[str] = 'url'


class ProfileKeys:
    # Flags
    Enabled: Final[str] = 'enabled'

    # JSON keys
    State: Final[str] = 'state'
    Details: Final[str] = 'details'
    LargeIcon: Final[str] = 'large_image'
    LargeText: Final[str] = 'large_text'
    SmallIcon: Final[str] = 'small_image'
    SmallText: Final[str] = 'small_text'
    Buttons: Final[str] = 'buttons'

    # Script features
    Script: Final[str] = 'script'

    # Format constants
    Client: Final[str] = 'client.'

    @staticmethod
    def parseResource(resource_key: str) -> Resources:
        if resource_key.startswith(ProfileKeys.Client):
            key = resource_key.replace(ProfileKeys.Client, '')
            return tuple(filter(
                lambda e: e.value == key,
                Resources.__members__.values()
            ))[0]
        else:
            raise ValueError('Currently, only resources in client can be used :(')
