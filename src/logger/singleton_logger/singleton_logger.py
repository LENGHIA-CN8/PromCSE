from typing import List, Optional
from logging import Handler
import logging
from logging import Logger
from threading import Lock
from logging import ERROR, WARNING, DEBUG, INFO
from logger.handlers import BaseHandlerConfig, HandlerBuilder


class SingletonLoggerConfig:
    """
    Config class for Singleton logger, (according to Singleton design pattern)
    """
    def __init__(
            self, handlers_config: List[BaseHandlerConfig],
            logger_name: Optional[str] = None, logger_level: Optional[int] = None
    ):
        """
        Init method
        :param handlers_config: list config of handlers
        :param logger_name: name of logger
        :param logger_level: level of logger
        """
        self.logger_name = logger_name
        self.logger_level = logger_level
        self.handlers_config = handlers_config

    @property
    def logger_name(self) -> str:
        return self._logger_name

    @logger_name.setter
    def logger_name(self, logger_name: Optional[str]):
        if logger_name is None:
            logger_name = "default_logger_name"
        else:
            assert isinstance(logger_name, str)
        self._logger_name: str = logger_name

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
    def handlers_config(self) -> List[BaseHandlerConfig]:
        return self._handlers_config

    @handlers_config.setter
    def handlers_config(self, handlers_config: List[BaseHandlerConfig]):
        assert isinstance(handlers_config, list)
        assert all(map(lambda x: isinstance(x, BaseHandlerConfig), handlers_config))
        self._handlers_config: List[BaseHandlerConfig] = handlers_config


class SingletonLogger:
    """
    Class for Singleton logger, according to Singleton design pattern
    """
    __config_has_been_set: bool = False  # mark when config of this logger is set or not
    __name: Optional[str] = None  # name of logger
    __handlers: Optional[List[Handler]] = None    # list of logger handlers
    __logger_level: Optional[int] = None    # process level of logger
    __logger: Optional[Logger] = None     # logger object
    __lock: Lock = Lock()  # for thread-safe

    @classmethod
    def get_instance(cls) -> Logger:
        """
        Get the logger instance
        :return: Logger
        """
        if cls.__logger is None:
            # if logger hasn't been inited
            cls.__lock.acquire()    # get the lock
            # re-check the logger
            if cls.__logger is None:
                # create the logger
                cls.__logger = logging.getLogger(name=cls.__name)
                cls.__logger.setLevel(level=cls.__logger_level)
                for handler in cls.__handlers:
                    cls.__logger.addHandler(handler)
            cls.__lock.release()    # release the lock
        return cls.__logger

    @classmethod
    def set_logger_config(cls, config: SingletonLoggerConfig):
        """
        Setting logger config; including name, handlers, logger level
        :param config: the config for the logger
        :return:
        """
        cls.__lock.acquire()    # get the log
        if not cls.__config_has_been_set:
            # config hasn't been set
            cls.__name = config.logger_name
            handlers: List[Handler] = list(map(HandlerBuilder.build_handler, config.handlers_config))
            cls.__handlers = handlers
            cls.__logger_level = config.logger_level
            cls.__config_has_been_set = True
        else:
            # config can only be set once
            print(f"Config for {cls.__name__} class have been set and can not be override")
        cls.__lock.release()


