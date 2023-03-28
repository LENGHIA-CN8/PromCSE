from abc import ABC, abstractmethod
from typing import Optional, List
from objects import User, Post


class BaseUserPostsReader(ABC):
    """
    Base class read posts related to a user (in some way: clicked by user, report by user,...)
    """
    @abstractmethod
    def read_user(
            self, user: User
    ) -> Optional[List[Post]]:
        """
        Read list posts related to user
        :param user: user to read
        :return: list posts related to user, or None
        """
        pass


class BaseUserPostsReaderConfig(ABC):
    """
    Base config class read posts related to a user (in some way: clicked by user, report by user,...)
    """
    pass
