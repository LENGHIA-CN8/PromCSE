from abc import ABC, abstractmethod
from typing import List, Optional
from objects import Post


class BaseAllPostsReader(ABC):
    """
    Base class for reading all posts
    The read method does not require any arguments
    """
    @abstractmethod
    def read_posts(self) -> Optional[List[Post]]:
        """
        Read list of posts
        :return: list of posts, None if failed
        """
        pass


class BaseAllPostsReaderConfig(ABC):
    """
    Base config class for reading all posts
    The read method does not require any arguments
    """
    pass
