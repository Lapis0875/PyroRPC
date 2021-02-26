from __future__ import annotations
from abc import abstractmethod, ABC
from src.type_hints import JSON


class JsonObject(ABC):
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
