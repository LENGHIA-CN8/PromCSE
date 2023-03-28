from typing import List
from objects import Post
from .base_post_writer import (
    BasePostWriter, BasePostWriterConfig
)


class ChainPostWriterVersion1(BasePostWriter):
    """
    Connect between writers to make a chain of responsibilities
    """
    def __init__(
            self, writers: List[BasePostWriter]
    ):
        """
        Init method
        :param writers: list of writers
        """
        super(ChainPostWriterVersion1, self).__init__()
        self.writers = writers

    @property
    def writers(self) -> List[BasePostWriter]:
        return self._writers

    @writers.setter
    def writers(self, writers: List[BasePostWriter]):
        assert isinstance(writers, list)
        assert all(map(lambda x: isinstance(x, BasePostWriter), writers))
        self._writers: List[BasePostWriter] = writers

    def write_post(self, post: Post) -> bool:
        """
        Write a post
        :param post: post to write
        :return: True if success, else False
        """
        status: bool = True
        for writer in self.writers:
            status = writer.write_post(post=post) and status
        return status

    def write_posts(self, posts: List[Post]) -> bool:
        """
        Write list of posts
        :param posts: posts to write
        :return: True if success, else False
        """
        status: bool = True
        for writer in self.writers:
            status = writer.write_posts(posts=posts) and status
        return status


class ChainPostWriterVersion1Config(BasePostWriterConfig):
    """
    Connect between writers to make a chain of responsibilities
    """
    def __init__(
            self, writers_config: List[BasePostWriterConfig]
    ):
        """
        Init method
        :param writers_config: list of writers
        """
        super(ChainPostWriterVersion1Config, self).__init__()
        self.writers_config = writers_config

    @property
    def writers_config(self) -> List[BasePostWriterConfig]:
        return self._writers_config

    @writers_config.setter
    def writers_config(self, writers_config: List[BasePostWriterConfig]):
        assert isinstance(writers_config, list)
        assert all(map(lambda x: isinstance(x, BasePostWriterConfig), writers_config))
        self._writers_config: List[BasePostWriterConfig] = writers_config
