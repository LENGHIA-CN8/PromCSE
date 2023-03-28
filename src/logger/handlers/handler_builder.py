from logging import Handler, Formatter, StreamHandler
from .version_1_stream_handler import StreamHandlerVersion1Config
from .version_1_email_handler import (
    EmailHandlerVersion1, EmailHandlerVersion1Config
)
from .base_handler_config import BaseHandlerConfig


class HandlerBuilder:
    """
    Class for building log record handler (according to Builder design pattern)
    """
    @classmethod
    def build_handler(cls, config: BaseHandlerConfig) -> Handler:
        """
        Build handler
        :param config: BaseHandlerConfig
        :return: Handler
        """
        if isinstance(config, EmailHandlerVersion1Config):
            handler: Handler = EmailHandlerVersion1(
                mailhost=config.mail_host, fromaddr=config.from_address,
                toaddrs=config.to_addresses, subject=config.subject,
                credentials=config.credentials
            )
            handler.setLevel(level=config.logger_level)
            formatter: Formatter = Formatter(config.format_string)
            handler.setFormatter(formatter)
        elif isinstance(config, StreamHandlerVersion1Config):
            handler = StreamHandler()
            handler.setLevel(level=config.logger_level)
            formatter: Formatter = Formatter(config.format_string)
            handler.setFormatter(formatter)
        else:
            raise ValueError(f"Invalid logger handler class: {config}")
        return handler
