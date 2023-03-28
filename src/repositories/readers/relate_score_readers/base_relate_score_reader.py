from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Dict
from objects import Post


class BaseRelateScoreReader(ABC):
    """
    Base class for reading relate score
    """
    @abstractmethod
    def read_post(self, post: Post) -> Optional[
        List[Tuple[Post, float]]
    ]:
        """
        Read relate score for a post
        :return: list of (post, score) or None
        """
        pass

    @abstractmethod
    def read_posts(self, posts: List[Post]) -> Optional[
        Dict[
            Post,
            List[Tuple[Post, float]]
        ]
    ]:
        """
        Read relate score for list of posts
        :return: mapping from post to list of (post, score); or None
        """
        pass


class BaseRelateScoreReaderConfig(ABC):
    """
    Base config class for reading relate score
    """
    pass
