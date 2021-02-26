from __future__ import annotations
from abc import abstractmethod, ABCMeta
from src.type_hints import JSON


class JsonObject(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def fromJson(cls, data: JSON) -> JsonObject:
        """
        Parse json data into JsonObject

        Args:
            data (Dict[str, Any]) : json data to parse.

        Returns:
            instance of JsonObject or its subclass
        """
        pass

    @abstractmethod
    def toJson(self) -> JSON:
        """
        Parse object into json data.

        Returns:
            json data of the object.
        """
        pass


class Scriptable(metaclass=ABCMeta):
    @property
    def script(self):
        """
        Script referenced by instance of Scriptable Subclass

        Returns:
             src.script_support.Script object
        """
        return self._script

    @abstractmethod
    def setScript(self, script):
        """
        Set internal script object.
        Args:
            script (src.script_support.Script) object
        """
