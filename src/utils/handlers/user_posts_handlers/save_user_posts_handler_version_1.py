from typing import List, Tuple
from repositories.writers import (
    BaseUserPostsWriter, BaseUserPostsWriterConfig
)
from objects import User, Post
from .base_user_posts_handler import (
    BaseUserPostsHandler,
    BaseUserPostsHandlerConfig
)
from utils.thread_utils import ThreadWithReturnValue
from logger import SingletonLogger


class SaveUserPostsHandlerVersion1(BaseUserPostsHandler):
    """
    Save users posts
    Running in a thread
    Only save top posts
    """
    def __init__(
            self, top_k: int, writer: BaseUserPostsWriter
    ):
        """
        Init method
        :param top_k: save top k posts
        :param writer: write data
        """
        super(SaveUserPostsHandlerVersion1, self).__init__()
        self.top_k = top_k
        self.writer = writer

    @property
    def top_k(self) -> int:
        return self._top_k

    @top_k.setter
    def top_k(self, top_k: int):
        assert isinstance(top_k, int)
        self._top_k: int = top_k

    @property
    def writer(self) -> BaseUserPostsWriter:
        return self._writer

    @writer.setter
    def writer(self, writer: BaseUserPostsWriter):
        assert isinstance(writer, BaseUserPostsWriter)
        self._writer: BaseUserPostsWriter = writer

    def handle(
            self, user: User, posts: List[Post]
    ):
        """
        Handle user posts result
        :param user: user
        :param posts: list posts
        """
        try:
            post_ids: List[int] = [
                post.post_id for post in posts[:self.top_k]
            ]
            thread = ThreadWithReturnValue(
                func=self.writer.write,
                func_kwargs={
                    "user": user,
                    "posts": [Post(post_id=post_id) for post_id in post_ids]
                }
            )
            thread.start()
        except:
            SingletonLogger.get_instance().exception(
                "Exception while save user posts"
            )


class SaveUserPostsHandlerVersion1Config(BaseUserPostsHandlerConfig):
    """
    Save user posts
    Running in a thread
    Only save top posts
    """
    def __init__(
            self, top_k: int, writer_config: BaseUserPostsWriterConfig
    ):
        """
        Init method
        :param top_k: save top k posts
        :param writer_config: write data
        """
        super(SaveUserPostsHandlerVersion1Config, self).__init__()
        self.top_k = top_k
        self.writer_config = writer_config

    @property
    def top_k(self) -> int:
        return self._top_k

    @top_k.setter
    def top_k(self, top_k: int):
        assert isinstance(top_k, int)
        self._top_k: int = top_k

    @property
    def writer_config(self) -> BaseUserPostsWriterConfig:
        return self._writer_config

    @writer_config.setter
    def writer_config(self, writer_config: BaseUserPostsWriterConfig):
        assert isinstance(writer_config, BaseUserPostsWriterConfig)
        self._writer_config: BaseUserPostsWriterConfig = writer_config

