from abc import ABC, abstractmethod
from typing import Optional, List
from objects import Post


class BasePostsCreator(ABC):
    """
    Base class for creating posts
    """
    @abstractmethod
    def create_posts(self) -> Optional[List[Post]]:
        """
        Create posts
        :return: list of posts, or None if failed
        """
        pass


class BasePostsCreatorConfig(ABC):
    """
    Base config class for creating posts
    """
    pass
