from .singleton_logger import SingletonLogger, SingletonLoggerConfig


class SingletonLoggerBuilder:
    """
    Class for building SingletonLogger class (according to Builder design pattern)
    """
    @classmethod
    def build_singleton_logger(cls, config: SingletonLoggerConfig):
        """
        Build singleton logger class
        :param config: config for the singleton logger
        :return:
        """
        SingletonLogger.set_logger_config(config=config)
