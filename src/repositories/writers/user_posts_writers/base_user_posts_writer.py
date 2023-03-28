from abc import ABC, abstractmethod
from typing import List
from objects import User, Post


class BaseUserPostsWriter(ABC):
    """
    Base class for writing user related posts
    """
    @abstractmethod
    def write(
            self, user: User, posts: List[Post]
    ) -> bool:
        """
        Write user posts
        :param user: User
        :param posts: posts
        """
        pass


class BaseUserPostsWriterConfig(ABC):
    """
    Base class for writing user related posts
    """
    pass
