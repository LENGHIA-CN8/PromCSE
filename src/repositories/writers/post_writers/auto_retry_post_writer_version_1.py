from typing import List, Optional
import time
from objects import Post
from .base_post_writer import (
    BasePostWriter, BasePostWriterConfig
)


class AutoRetryPostWriterVersion1(BasePostWriter):
    """
    Class for auto retry writing if failed
    """
    def __init__(
            self, wrapped_writer: BasePostWriter,
            num_tries: int, time_between: Optional[float]
    ):
        """
        Init method
        :param wrapped_writer: wrapped writer
        :param num_tries: maximum number of try times
        :param time_between: time between try times
        """
        super(AutoRetryPostWriterVersion1, self).__init__()
        self.wrapped_writer = wrapped_writer
        self.num_tries = num_tries
        self.time_between = time_between

    @property
    def wrapped_writer(self) -> BasePostWriter:
        return self._wrapped_writer

    @wrapped_writer.setter
    def wrapped_writer(self, wrapped_writer: BasePostWriter):
        assert isinstance(wrapped_writer, BasePostWriter)
        self._wrapped_writer: BasePostWriter = wrapped_writer

    @property
    def num_tries(self) -> int:
        return self._num_tries

    @num_tries.setter
    def num_tries(self, num_tries: int):
        assert isinstance(num_tries, int)
        self._num_tries: int = num_tries

    @property
    def time_between(self) -> Optional[float]:
        return self._time_between

    @time_between.setter
    def time_between(self, time_between: Optional[float]):
        if time_between is not None:
            assert isinstance(time_between, float)
        self._time_between: Optional[float] = time_between

    def write_post(self, post: Post) -> bool:
        """
        Write a post
        :param post: post to write
        :return: True if success, else False
        """
        for try_time in range(self.num_tries):
            status: bool = self.wrapped_writer.write_post(post=post)
            if status:
                return True
            if (
                    self.time_between is not None and
                    try_time + 1 < self.num_tries
            ):
                time.sleep(self.time_between)
        return False

    def write_posts(self, posts: List[Post]) -> bool:
        """
        Write list of posts
        :param posts: posts to write
        :return: True if success, else False
        """
        for try_time in range(self.num_tries):
            status: bool = self.wrapped_writer.write_posts(posts=posts)
            if status:
                return True
            if (
                    self.time_between is not None and
                    try_time + 1 < self.num_tries
            ):
                time.sleep(self.time_between)
        return False


class AutoRetryPostsWriterVersion1Config(BasePostWriterConfig):
    """
    Config class for auto retry writing if failed
    """
    def __init__(
            self, wrapped_writer_config: BasePostWriterConfig,
            num_tries: int, time_between: Optional[float]
    ):
        """
        Init method
        :param wrapped_writer_config: wrapped writer
        :param num_tries: maximum number of try times
        :param time_between: time between try times
        """
        super().__init__()
        self.wrapped_writer_config = wrapped_writer_config
        self.num_tries = num_tries
        self.time_between = time_between

    @property
    def wrapped_writer_config(self) -> BasePostWriterConfig:
        return self._wrapped_writer_config

    @wrapped_writer_config.setter
    def wrapped_writer_config(self, wrapped_writer_config: BasePostWriterConfig):
        assert isinstance(wrapped_writer_config, BasePostWriterConfig)
        self._wrapped_writer_config: BasePostWriterConfig = wrapped_writer_config

    @property
    def num_tries(self) -> int:
        return self._num_tries

    @num_tries.setter
    def num_tries(self, num_tries: int):
        assert isinstance(num_tries, int)
        self._num_tries: int = num_tries

    @property
    def time_between(self) -> Optional[float]:
        return self._time_between

    @time_between.setter
    def time_between(self, time_between: Optional[float]):
        if time_between is not None:
            assert isinstance(time_between, float)
        self._time_between: Optional[float] = time_between
