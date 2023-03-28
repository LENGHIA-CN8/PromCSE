from abc import ABC, abstractmethod
from objects import User, Post
from typing import List


class BaseUserPostsHandler(ABC):
    """
    Base class for handle user posts
    """
    @abstractmethod
    def handle(
            self, user: User, posts: List[Post]
    ):
        """
        Handle user result
        :param user: user
        :param posts: list posts
        """
        pass


class BaseUserPostsHandlerConfig(ABC):
    """
    Base config class for handle user posts
    """
    pass
