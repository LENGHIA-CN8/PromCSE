from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Dict
from objects import User, Post


class BasePerScoreReader(ABC):
    """
    Base class for reading per score
    """
    @abstractmethod
    def read_user(self, user: User) -> Optional[
        List[Tuple[Post, float]]
    ]:
        """
        Read per score for a user
        :return: list of (post, score) or None
        """
        pass

    @abstractmethod
    def read_users(self, users: List[User]) -> Optional[
        Dict[
            User,
            List[Tuple[Post, float]]
        ]
    ]:
        """
        Read per score for list of users
        :return: mapping from user to list of (post, score); or None
        """
        pass


class BasePerScoreReaderConfig(ABC):
    """
    Base config class for reading per score
    """
    pass
