from typing import List
from objects import Post
from .base_posts_filter import (
    BasePostsFilter, BasePostsFilterConfig
)
from abc import ABC, abstractmethod


class BaseElementWisePostsFilter(BasePostsFilter, ABC):
    """
    Base class for filter invalid posts element-wise
    """
    @abstractmethod
    def _is_valid(self, post: Post) -> bool:
        """
        Check if post is valid
        :param post: post to check
        :return: True if valid, else False
        """
        pass

    def filter_posts(
            self, posts: List[Post]
    ) -> List[Post]:
        """
        Remove invalid posts
        :param posts: list of posts
        :return: list valid posts
        """
        return [
            post for post in posts
            if self._is_valid(post=post)
        ]


class BaseElementWisePostsFilterConfig(BasePostsFilterConfig, ABC):
    """
    Base class for filter invalid posts element-wise
    """
    pass
