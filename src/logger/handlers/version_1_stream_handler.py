from typing import Optional
from logging import ERROR, WARNING, DEBUG, INFO
from .base_handler_config import BaseHandlerConfig


class StreamHandlerVersion1Config(BaseHandlerConfig):
    """
    Config class for handle log record via print to a stream version 1
    """
    def __init__(
            self, logger_level: Optional[int] = None,
            format_string: Optional[str] = None
    ):
        """
        Init method
        :param logger_level: logger level
        :param format_string: format string
        """
        self.logger_level = logger_level
        self.format_string = format_string

    @property
    def logger_level(self) -> int:
        return self._logger_level

    @logger_level.setter
    def logger_level(self, logger_level: Optional[int]):
        if logger_level is None:
            logger_level = DEBUG
        else:
            assert isinstance(logger_level, int)
            if logger_level not in {ERROR, WARNING, DEBUG, INFO}:
                print(f"Invalid logger level {logger_level}")
                logger_level = DEBUG
        self._logger_level: int = logger_level

    @property
    def format_string(self) -> str:
        return self._format_string

    @format_string.setter
    def format_string(self, format_string: Optional[str]):
        if format_string is None:
            format_string = '%(levelname)s   %(asctime)s   %(message)s'
        else:
            assert isinstance(format_string, str)
        self._format_string: str = format_string
