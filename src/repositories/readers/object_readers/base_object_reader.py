from abc import ABC, abstractmethod
from typing import Optional


class BaseObjectReader(ABC):
    """
    Base class for reading general object
    """
    @abstractmethod
    def read_object(self) -> Optional[object]:
        """
        Read object
        :return: object if success, else None
        """
        pass


class BaseObjectReaderConfig(ABC):
    """
    Base config class for reading general object
    """
    pass
