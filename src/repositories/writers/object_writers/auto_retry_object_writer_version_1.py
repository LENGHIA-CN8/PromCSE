from .base_object_writer import (
    BaseObjectWriter, BaseObjectWriterConfig
)
from typing import Optional
import time


class AutoRetryObjectWriterVersion1(BaseObjectWriter):
    """
    Class for auto retry writing any object if failed
    """
    def __init__(
            self, wrapped_writer: BaseObjectWriter,
            num_tries: int, time_break: Optional[float] = None
    ):
        """
        Init method
        :param wrapped_writer: inner writer
        :param num_tries: maximum number of try time
        :param time_break: time between try time
        """
        super().__init__()
        self.wrapped_writer = wrapped_writer
        self.num_tries = num_tries
        self.time_break = time_break

    @property
    def wrapped_writer(self) -> BaseObjectWriter:
        return self._wrapped_writer

    @wrapped_writer.setter
    def wrapped_writer(self, wrapped_writer: BaseObjectWriter):
        assert isinstance(wrapped_writer, BaseObjectWriter)
        self._wrapped_writer: BaseObjectWriter = wrapped_writer

    @property
    def num_tries(self) -> int:
        return self._num_tries

    @num_tries.setter
    def num_tries(self, num_tries: int):
        assert isinstance(num_tries, int)
        self._num_tries: int = num_tries

    @property
    def time_break(self) -> Optional[float]:
        return self._time_break

    @time_break.setter
    def time_break(self, time_break: Optional[float]):
        if time_break is not None:
            assert isinstance(time_break, float)
        self._time_break: Optional[float] = time_break

    def write_object(self, data: object) -> bool:
        """
        Write object
        :param data: data to write
        :return: True if success, else False
        """
        for try_time in range(self.num_tries):
            status: bool = self.wrapped_writer.write_object(data=data)
            if status:
                return status
            if self.time_break is not None and try_time + 1 < self.num_tries:
                time.sleep(self.time_break)
        return False


class AutoRetryObjectWriterVersion1Config(BaseObjectWriterConfig):
    """
    Config class for auto retry writing any object if failed
    """

    def __init__(
            self, wrapped_writer_config: BaseObjectWriterConfig,
            num_tries: int, time_break: Optional[float] = None
    ):
        """
        Init method
        :param wrapped_writer_config: inner writer
        :param num_tries: maximum number of try time
        :param time_break: time between try time
        """
        super().__init__()
        self.wrapped_writer_config = wrapped_writer_config
        self.num_tries = num_tries
        self.time_break = time_break

    @property
    def wrapped_writer_config(self) -> BaseObjectWriterConfig:
        return self._wrapped_writer_config

    @wrapped_writer_config.setter
    def wrapped_writer_config(self, wrapped_writer_config: BaseObjectWriterConfig):
        assert isinstance(wrapped_writer_config, BaseObjectWriterConfig)
        self._wrapped_writer_config: BaseObjectWriterConfig = wrapped_writer_config

    @property
    def num_tries(self) -> int:
        return self._num_tries

    @num_tries.setter
    def num_tries(self, num_tries: int):
        assert isinstance(num_tries, int)
        self._num_tries: int = num_tries

    @property
    def time_break(self) -> Optional[float]:
        return self._time_break

    @time_break.setter
    def time_break(self, time_break: Optional[float]):
        if time_break is not None:
            assert isinstance(time_break, float)
        self._time_break: Optional[float] = time_break
