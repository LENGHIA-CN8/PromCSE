from typing import List
from objects import Post
from .base_posts_handler import (
    BasePostsHandler, BasePostsHandlerConfig
)
from repositories.writers import (
    BasePostWriter, BasePostWriterConfig
)


class SavePostsHandlerVersion1(BasePostsHandler):
    """
    Save posts by using post writer object
    """
    def __init__(self, writer: BasePostWriter):
        """
        Init method
        :param writer: post writer object
        """
        super(SavePostsHandlerVersion1, self).__init__()
        self.writer = writer

    @property
    def writer(self) -> BasePostWriter:
        return self._writer

    @writer.setter
    def writer(self, writer: BasePostWriter):
        assert isinstance(writer, BasePostWriter)
        self._writer: BasePostWriter = writer

    def handle_posts(
            self, posts: List[Post]
    ):
        """
        Handle posts
        :param posts: created posts to handle
        """
        self.writer.write_posts(
            posts=posts
        )


class SavePostsHandlerVersion1Config(BasePostsHandlerConfig):
    """
    Config for save posts by using post writer object
    """
    def __init__(self, writer_config: BasePostWriterConfig):
        """
        Init method
        :param writer_config: post writer object
        """
        super(SavePostsHandlerVersion1Config, self).__init__()
        self.writer_config = writer_config

    @property
    def writer_config(self) -> BasePostWriterConfig:
        return self._writer_config

    @writer_config.setter
    def writer_config(self, writer_config: BasePostWriterConfig):
        assert isinstance(writer_config, BasePostWriterConfig)
        self._writer_config: BasePostWriterConfig = writer_config
