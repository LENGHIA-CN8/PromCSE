from abc import ABC, abstractmethod


class BaseObjectWriter(ABC):
    """
    Base class for write general object
    """
    @abstractmethod
    def write_object(self, data: object) -> bool:
        """
        Write an object
        :param data: object to write
        :return: True if success, else False
        """
        pass


class BaseObjectWriterConfig(ABC):
    """
    Base config class for write general object
    """
    pass

