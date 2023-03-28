from typing import List
from abc import ABC, abstractmethod
from objects import Post
from .base_post_reader import (
    BasePostReader, BasePostReaderConfig
)


class BaseCheckAndReadPostReaderVersion1(BasePostReader, ABC):
    """
    Base class for check if post need to read before reading post
    """
    def __init__(
            self, wrapped_reader: BasePostReader
    ):
        """
        Init method
        :param wrapped_reader: wrapped post reader
        """
        super(BaseCheckAndReadPostReaderVersion1, self).__init__()
        self.wrapped_reader = wrapped_reader

    @property
    def wrapped_reader(self) -> BasePostReader:
        return self._wrapped_reader

    @wrapped_reader.setter
    def wrapped_reader(self, wrapped_reader: BasePostReader):
        assert isinstance(wrapped_reader, BasePostReader)
        self._wrapped_reader: BasePostReader = wrapped_reader

    @abstractmethod
    def _is_need_to_read(self, post: Post) -> bool:
        """
        Check if we need to read post info
        :param post: post to check
        :return: True if need to read, else False
        """
        pass

    def read_post(self, post: Post) -> bool:
        """
        Read info of a post
        :param post: post to read info
        :return: True if success, else False
        """
        if self._is_need_to_read(post=post):
            return self.wrapped_reader.read_post(
                post=post
            )
        else:
            return True

    def read_posts(self, posts: List[Post]) -> bool:
        """
        Read info of a collection of posts
        :param posts: posts to read info
        :return: True if success, else False
        """
        posts: List[Post] = [
            post for post in posts
            if self._is_need_to_read(post=post)
        ]
        if posts:
            return self.wrapped_reader.read_posts(
                posts=posts
            )
        else:
            return True


class BaseCheckAndReadPostReaderVersion1Config(BasePostReaderConfig, ABC):
    """
    Base config for check if post need to read before reading post
    """
    def __init__(
            self, wrapped_reader_config: BasePostReaderConfig
    ):
        """
        Init method
        :param wrapped_reader_config: wrapped post reader
        """
        super(BaseCheckAndReadPostReaderVersion1Config, self).__init__()
        self.wrapped_reader_config = wrapped_reader_config

    @property
    def wrapped_reader_config(self) -> BasePostReaderConfig:
        return self._wrapped_reader_config

    @wrapped_reader_config.setter
    def wrapped_reader_config(self, wrapped_reader_config: BasePostReaderConfig):
        assert isinstance(wrapped_reader_config, BasePostReaderConfig)
        self._wrapped_reader_config: BasePostReaderConfig = wrapped_reader_config

