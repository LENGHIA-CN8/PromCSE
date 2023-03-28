from abc import ABC, abstractmethod
from objects import User
from typing import List


class BaseUserReader(ABC):
    """
    Base class for reading user info
    """
    @abstractmethod
    def read_user(self, user: User) -> bool:
        """
        Read user info
        :param user: user to read info
        :return: True if success, else False
        """
        pass

    @abstractmethod
    def read_users(self, users: List[User]) -> bool:
        """
        Read list users info
        :param users: list users to read info
        :return: True if success, else False
        """
        pass


class BaseUserReaderConfig(ABC):
    """
    Base config class for reading user info
    """
    pass
