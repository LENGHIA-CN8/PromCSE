from abc import ABC, abstractmethod
from typing import Optional, List
from objects import User


class BaseAllUsersReader(ABC):
    """
    Base class for reading all users
    """
    @abstractmethod
    def read_users(self) -> Optional[List[User]]:
        """
        Read list of users
        :return: list of users or None
        """
        pass


class BaseAllUsersReaderConfig(ABC):
    """
    Base config class for reading all users
    """
    pass

