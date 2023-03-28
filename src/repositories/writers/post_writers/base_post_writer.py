from abc import ABC, abstractmethod
from typing import List
from objects import Post


class BasePostWriter(ABC):
    """
    Base class for writing post
    """
    @abstractmethod
    def write_post(self, post: Post) -> bool:
        """
        Write a post
        :param post: post to write
        :return: True if success, else False
        """
        pass

    @abstractmethod
    def write_posts(self, posts: List[Post]) -> bool:
        """
        Write list of posts
        :param posts: posts to write
        :return: True if success, else False
        """
        pass


class BasePostWriterConfig(ABC):
    """
    Base config class for writing post
    """
    pass
