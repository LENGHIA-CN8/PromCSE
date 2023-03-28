from .base_object_writer import (
    BaseObjectWriter, BaseObjectWriterConfig
)
from typing import Optional
import time


class ChainObjectWriterVersion1(BaseObjectWriter):
    """
    Connect between writers to make a chain of responsibilities
    """
    def __init__(
            self, wrapped_writer: BaseObjectWriter,
            next_writer: Optional[BaseObjectWriter] = None,
            time_break: Optional[float] = None
    ):
        """
        Init method
        :param wrapped_writer: writer on current node
        :param next_writer: writer on next node
        :param time_break: time between writer
        """
        super().__init__()
        self.wrapped_writer = wrapped_writer
        self.next_writer = next_writer
        self.time_break = time_break

    @property
    def wrapped_writer(self) -> BaseObjectWriter:
        return self._wrapped_writer

    @wrapped_writer.setter
    def wrapped_writer(self, wrapped_writer: BaseObjectWriter):
        assert isinstance(wrapped_writer, BaseObjectWriter)
        self._wrapped_writer: BaseObjectWriter = wrapped_writer

    @property
    def next_writer(self) -> Optional[BaseObjectWriter]:
        return self._next_writer

    @next_writer.setter
    def next_writer(self, next_writer: Optional[BaseObjectWriter]):
        if next_writer is not None:
            assert isinstance(next_writer, BaseObjectWriter)
        self._next_writer: Optional[BaseObjectWriter] = next_writer

    def write_object(self, data: object) -> bool:
        """
        Write object
        :param data: data to write
        :return: True if success, else False
        """
        status: bool = self.wrapped_writer.write_object(data=data)
        if self.next_writer is not None:
            if self.time_break is not None:
                time.sleep(self.time_break)
            return self.next_writer.write_object(
                data=data
            ) and status
        else:
            return status


class ChainObjectWriterVersion1Config(BaseObjectWriterConfig):
    """
    Config class for connect between writers to make a chain of responsibilities
    """
    def __init__(
            self, wrapped_writer_config: BaseObjectWriterConfig,
            next_writer_config: Optional[BaseObjectWriterConfig] = None,
            time_break: Optional[float] = None
    ):
        """
        Init method
        :param wrapped_writer_config: writer on current node
        :param next_writer_config: writer on next node
        :param time_break: time between writer
        """
        super().__init__()
        self.wrapped_writer_config = wrapped_writer_config
        self.next_writer_config = next_writer_config
        self.time_break = time_break

    @property
    def wrapped_writer_config(self) -> BaseObjectWriterConfig:
        return self._wrapped_writer_config

    @wrapped_writer_config.setter
    def wrapped_writer_config(self, wrapped_writer_config: BaseObjectWriterConfig):
        assert isinstance(wrapped_writer_config, BaseObjectWriterConfig)
        self._wrapped_writer_config: BaseObjectWriterConfig = wrapped_writer_config

    @property
    def next_writer_config(self) -> Optional[BaseObjectWriterConfig]:
        return self._next_writer_config

    @next_writer_config.setter
    def next_writer_config(self, next_writer_config: Optional[BaseObjectWriterConfig]):
        if next_writer_config is not None:
            assert isinstance(next_writer_config, BaseObjectWriterConfig)
        self._next_writer_config: Optional[BaseObjectWriterConfig] = next_writer_config

