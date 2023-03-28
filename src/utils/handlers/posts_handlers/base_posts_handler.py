from abc import ABC, abstractmethod
from objects import Post
from typing import List


class BasePostsHandler(ABC):
    """
    Base class for handle created posts
    """
    @abstractmethod
    def handle_posts(
            self, posts: List[Post]
    ):
        """
        Handle posts
        :param posts: created posts to handle
        """
        pass


class BasePostsHandlerConfig(ABC):
    """
    Base config class for handle created posts
    """
    pass
