from .base_object_reader import (
    BaseObjectReader, BaseObjectReaderConfig
)
from typing import Optional
import time


class ChainObjectReaderVersion1(BaseObjectReader):
    """
    Connect between readers to make a chain of responsibilities
    """
    def __init__(
            self, wrapped_reader: BaseObjectReader,
            next_reader: Optional[BaseObjectReader] = None,
            time_break: Optional[float] = None
    ):
        """
        Init method
        :param wrapped_reader: reader on current node
        :param next_reader: reader on next node
        :param time_break: time between reader
        """
        super().__init__()
        self.wrapped_reader = wrapped_reader
        self.next_reader = next_reader
        self.time_break = time_break

    @property
    def wrapped_reader(self) -> BaseObjectReader:
        return self._wrapped_reader

    @wrapped_reader.setter
    def wrapped_reader(self, wrapped_reader: BaseObjectReader):
        assert isinstance(wrapped_reader, BaseObjectReader)
        self._wrapped_reader: BaseObjectReader = wrapped_reader

    @property
    def next_reader(self) -> Optional[BaseObjectReader]:
        return self._next_reader

    @next_reader.setter
    def next_reader(self, next_reader: Optional[BaseObjectReader]):
        if next_reader is not None:
            assert isinstance(next_reader, BaseObjectReader)
        self._next_reader: Optional[BaseObjectReader] = next_reader

    def read_object(self) -> Optional[object]:
        """
        Read object
        :return: data if success, else None
        """
        data: Optional[object] = self.wrapped_reader.read_object()
        if data is not None or self.next_reader is None:
            return data
        if self.time_break is not None:
            time.sleep(self.time_break)
        return self.next_reader.read_object()


class ChainObjectReaderVersion1Config(BaseObjectReaderConfig):
    """
    Config class for connect between reader to make a chain of responsibilities
    """
    def __init__(
            self, wrapped_reader_config: BaseObjectReaderConfig,
            next_reader_config: Optional[BaseObjectReaderConfig] = None,
            time_break: Optional[float] = None
    ):
        """
        Init method
        :param wrapped_reader_config: reader on current node
        :param next_reader_config: reader on next node
        :param time_break: time between reader
        """
        super().__init__()
        self.wrapped_reader_config = wrapped_reader_config
        self.next_reader_config = next_reader_config
        self.time_break = time_break

    @property
    def wrapped_reader_config(self) -> BaseObjectReaderConfig:
        return self._wrapped_reader_config

    @wrapped_reader_config.setter
    def wrapped_reader_config(self, wrapped_reader_config: BaseObjectReaderConfig):
        assert isinstance(wrapped_reader_config, BaseObjectReaderConfig)
        self._wrapped_reader_config: BaseObjectReaderConfig = wrapped_reader_config

    @property
    def next_reader_config(self) -> Optional[BaseObjectReaderConfig]:
        return self._next_reader_config

    @next_reader_config.setter
    def next_reader_config(self, next_reader_config: Optional[BaseObjectReaderConfig]):
        if next_reader_config is not None:
            assert isinstance(next_reader_config, BaseObjectReaderConfig)
        self._next_reader_config: Optional[BaseObjectReaderConfig] = next_reader_config
