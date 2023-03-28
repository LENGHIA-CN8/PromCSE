from .base_object_reader import (
    BaseObjectReader, BaseObjectReaderConfig
)
from typing import Optional
import time


class AutoRetryObjectReaderVersion1(BaseObjectReader):
    """
    Class for auto retry reading any object if failed
    """
    def __init__(
            self, wrapped_reader: BaseObjectReader,
            num_tries: int, time_break: Optional[float] = None
    ):
        """
        Init method
        :param wrapped_reader: inner reader
        :param num_tries: maximum number of try time
        :param time_break: time between try time
        """
        super().__init__()
        self.wrapped_reader = wrapped_reader
        self.num_tries = num_tries
        self.time_break = time_break

    @property
    def wrapped_reader(self) -> BaseObjectReader:
        return self._wrapped_reader

    @wrapped_reader.setter
    def wrapped_reader(self, wrapped_reader: BaseObjectReader):
        assert isinstance(wrapped_reader, BaseObjectReader)
        self._wrapped_reader: BaseObjectReader = wrapped_reader

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

    def read_object(self) -> Optional[object]:
        """
        Read object
        :return: data if success, else None
        """
        for try_time in range(self.num_tries):
            data: Optional[object] = self.wrapped_reader.read_object()
            if data is not None:
                return data
            if self.time_break is not None and try_time + 1 < self.num_tries:
                time.sleep(self.time_break)
        return None


class AutoRetryObjectReaderVersion1Config(BaseObjectReaderConfig):
    """
    Config class for auto retry reading any object if failed
    """

    def __init__(
            self, wrapped_reader_config: BaseObjectReaderConfig,
            num_tries: int, time_break: Optional[float] = None
    ):
        """
        Init method
        :param wrapped_reader_config: inner reader
        :param num_tries: maximum number of try time
        :param time_break: time between try time
        """
        super().__init__()
        self.wrapped_reader_config = wrapped_reader_config
        self.num_tries = num_tries
        self.time_break = time_break

    @property
    def wrapped_reader_config(self) -> BaseObjectReaderConfig:
        return self._wrapped_reader_config

    @wrapped_reader_config.setter
    def wrapped_reader_config(self, wrapped_reader_config: BaseObjectReaderConfig):
        assert isinstance(wrapped_reader_config, BaseObjectReaderConfig)
        self._wrapped_reader_config: BaseObjectReaderConfig = wrapped_reader_config

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
