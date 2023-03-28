from typing import List, Optional, Tuple, Dict
import time
from objects import Post, User
from .base_per_score_writer import (
    BasePerScoreWriter, BasePerScoreWriterConfig
)


class AutoRetryPerScoreWriterVersion1(BasePerScoreWriter):
    """
    Class for auto retry writing if failed
    """
    def __init__(
            self, wrapped_writer: BasePerScoreWriter,
            num_tries: int, time_between: Optional[float]
    ):
        """
        Init method
        :param wrapped_writer: wrapped writer
        :param num_tries: maximum number of try times
        :param time_between: time between try times
        """
        super(AutoRetryPerScoreWriterVersion1, self).__init__()
        self.wrapped_writer = wrapped_writer
        self.num_tries = num_tries
        self.time_between = time_between

    @property
    def wrapped_writer(self) -> BasePerScoreWriter:
        return self._wrapped_writer

    @wrapped_writer.setter
    def wrapped_writer(self, wrapped_writer: BasePerScoreWriter):
        assert isinstance(wrapped_writer, BasePerScoreWriter)
        self._wrapped_writer: BasePerScoreWriter = wrapped_writer

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
            self, user: User,
            posts_scores: List[Tuple[Post, float]]
    ) -> bool:
        """
        Write per score
        :param user: user
        :param posts_scores: list scores of candidates. list of tuple (post, score)
        :return: True if success, else False
        """
        for try_time in range(self.num_tries):
            status: bool = self.wrapped_writer.write_score(
                user=user, posts_scores=posts_scores
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
            self, user_to_result: Dict[
                User,
                List[Tuple[Post, float]]
            ]
    ) -> bool:
        """
        Write multiple per scores
        :param user_to_result: mapping from user to list of tuple (post, score)
        :return True if success, else False
        """
        for try_time in range(self.num_tries):
            status: bool = self.wrapped_writer.write_scores(
                user_to_result=user_to_result
            )
            if status:
                return True
            if (
                    self.time_between is not None and
                    try_time + 1 < self.num_tries
            ):
                time.sleep(self.time_between)
        return False


class AutoRetryPerScoreWriterVersion1Config(BasePerScoreWriterConfig):
    """
    Config class for auto retry writing if failed
    """
    def __init__(
            self, wrapped_writer_config: BasePerScoreWriterConfig,
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
    def wrapped_writer_config(self) -> BasePerScoreWriterConfig:
        return self._wrapped_writer_config

    @wrapped_writer_config.setter
    def wrapped_writer_config(self, wrapped_writer_config: BasePerScoreWriterConfig):
        assert isinstance(wrapped_writer_config, BasePerScoreWriterConfig)
        self._wrapped_writer_config: BasePerScoreWriterConfig = wrapped_writer_config

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
