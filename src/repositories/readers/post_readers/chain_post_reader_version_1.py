from objects import Post
from .base_post_reader import (
    BasePostReader, BasePostReaderConfig
)
from typing import List


class ChainPostReaderVersion1(BasePostReader):
    """
    Chain of readers
    """
    def __init__(
            self, wrapped_readers: List[BasePostReader]
    ):
        """
        Init method
        :param wrapped_readers: list of reader
        """
        super(ChainPostReaderVersion1, self).__init__()
        self.wrapped_readers = wrapped_readers

    @property
    def wrapped_readers(self) -> List[BasePostReader]:
        return self._wrapped_readers

    @wrapped_readers.setter
    def wrapped_readers(self, wrapped_readers: List[BasePostReader]):
        assert isinstance(wrapped_readers, list)
        assert all(map(lambda x: isinstance(x, BasePostReader), wrapped_readers))
        self._wrapped_readers: List[BasePostReader] = wrapped_readers

    def read_post(self, post: Post) -> bool:
        """
        Read info of a post
        :param post: post to read info
        :return: True if success, else False
        """
        status: bool = True
        for reader in self.wrapped_readers:
            status = reader.read_post(
                post=post
            ) and status
        return status

    def read_posts(self, posts: List[Post]) -> bool:
        """
        Read info of a collection of posts
        :param posts: posts to read info
        :return: True if success, else False
        """
        status: bool = True
        for reader in self.wrapped_readers:
            status = reader.read_posts(
                posts=posts
            ) and status
        return status


class ChainPostReaderVersion1Config(BasePostReaderConfig):
    """
    Chain of readers
    """
    def __init__(
            self, wrapped_readers_config: List[BasePostReaderConfig]
    ):
        """
        Init method
        :param wrapped_readers_config: list of reader
        """
        super(ChainPostReaderVersion1Config, self).__init__()
        self.wrapped_readers_config = wrapped_readers_config

    @property
    def wrapped_readers_config(self) -> List[BasePostReaderConfig]:
        return self._wrapped_readers_config

    @wrapped_readers_config.setter
    def wrapped_readers_config(self, wrapped_readers_config: List[BasePostReaderConfig]):
        assert isinstance(wrapped_readers_config, list)
        assert all(map(lambda x: isinstance(x, BasePostReaderConfig), wrapped_readers_config))
        self._wrapped_readers_config: List[BasePostReaderConfig] = wrapped_readers_config
