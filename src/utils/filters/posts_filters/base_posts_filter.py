from abc import ABC, abstractmethod
from typing import List
from objects import Post


class BasePostsFilter(ABC):
    """
    Base class for filtering posts: removing invalid posts
    """
    @abstractmethod
    def filter_posts(
            self, posts: List[Post]
    ) -> List[Post]:
        """
        Remove invalid posts
        :param posts: list of posts
        :return: list valid posts
        """
        pass


class BasePostsFilterConfig(ABC):
    """
    Base config class for filtering posts: removing invalid posts
    """
    pass
