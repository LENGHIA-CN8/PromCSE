from abc import ABC, abstractmethod
from objects import Post
from typing import List


class BasePostReader(ABC):
    """
    Base class for reading posts info
    The info will be updated inplace into object properties
    """
    @abstractmethod
    def read_post(self, post: Post) -> bool:
        """
        Read info of a post
        :param post: post to read info
        :return: True if success, else False
        """
        pass

    @abstractmethod
    def read_posts(self, posts: List[Post]) -> bool:
        """
        Read info of a collection of posts
        :param posts: posts to read info
        :return: True if success, else False
        """
        pass


class BasePostReaderConfig(ABC):
    """
    Base config class for reading posts info
    """
    pass
