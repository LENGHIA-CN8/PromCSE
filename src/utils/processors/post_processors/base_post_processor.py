from abc import ABC, abstractmethod
from objects import Post
from typing import List


class BasePostProcessor(ABC):
    """
    Base class for process post (modify its properties)
    All modification will be updated inplace
    """
    @abstractmethod
    def process_post(self, post: Post):
        """
        Process post inplace
        :param post: post to process
        :return: None
        """
        pass

    @abstractmethod
    def process_posts(self, posts: List[Post]):
        """
        Process collection of posts
        :param posts: collection of posts to process
        :return: None
        """
        pass


class BasePostProcessorConfig(ABC):
    """
    Base config class for process post (modify its properties)
    All modification will be updated inplace
    """
    pass
