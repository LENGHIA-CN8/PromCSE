from typing import List, Optional, Tuple, Dict
import time
from objects import Post
from .base_relate_score_writer import (
    BaseRelateScoreWriter, BaseRelateScoreWriterConfig
)


class AutoRetryRelateScoreWriterVersion1(BaseRelateScoreWriter):
    """
    Class for auto retry writing if failed
    """
    def __init__(
            self, wrapped_writer: BaseRelateScoreWriter,
            num_tries: int, time_between: Optional[float]
    ):
        """
        Init method
        :param wrapped_writer: wrapped writer
        :param num_tries: maximum number of try times
        :param time_between: time between try times
        """
        super(AutoRetryRelateScoreWriterVersion1, self).__init__()
        self.wrapped_writer = wrapped_writer
        self.num_tries = num_tries
        self.time_between = time_between

    @property
    def wrapped_writer(self) -> BaseRelateScoreWriter:
        return self._wrapped_writer

    @wrapped_writer.setter
    def wrapped_writer(self, wrapped_writer: BaseRelateScoreWriter):
        assert isinstance(wrapped_writer, BaseRelateScoreWriter)
        self._wrapped_writer: BaseRelateScoreWriter = wrapped_writer

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

    def write_score(
            self, seed_post: Post,
            posts_scores: List[Tuple[Post, float]]
    ) -> bool:
        """
        Write relate score
        :param seed_post: seed post
        :param posts_scores: list scores of candidates. list of tuple (post, score)
        :return: True if success, else False
        """
        for try_time in range(self.num_tries):
            status: bool = self.wrapped_writer.write_score(
                seed_post=seed_post, posts_scores=posts_scores
            )
            if status:
                return True
            if (
                    self.time_between is not None and
                    try_time + 1 < self.num_tries
            ):
                time.sleep(self.time_between)
        return False

    def write_scores(
            self, seed_post_to_result: Dict[
                Post,
                List[Tuple[Post, float]]
            ]
    ) -> bool:
        """
        Write multiple relate scores
        :param seed_post_to_result: mapping from seed post to list of tuple (post, score)
        :return True if success, else False
        """
        for try_time in range(self.num_tries):
            status: bool = self.wrapped_writer.write_scores(
                seed_post_to_result=seed_post_to_result
            )
            if status:
                return True
            if (
                    self.time_between is not None and
                    try_time + 1 < self.num_tries
            ):
                time.sleep(self.time_between)
        return False


class AutoRetryRelateScoreWriterVersion1Config(BaseRelateScoreWriterConfig):
    """
    Config class for auto retry writing if failed
    """
    def __init__(
            self, wrapped_writer_config: BaseRelateScoreWriterConfig,
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
    def wrapped_writer_config(self) -> BaseRelateScoreWriterConfig:
        return self._wrapped_writer_config

    @wrapped_writer_config.setter
    def wrapped_writer_config(self, wrapped_writer_config: BaseRelateScoreWriterConfig):
        assert isinstance(wrapped_writer_config, BaseRelateScoreWriterConfig)
        self._wrapped_writer_config: BaseRelateScoreWriterConfig = wrapped_writer_config

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
