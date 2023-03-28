"""
This package contains class for logging
"""

from .singleton_logger import (
    SingletonLogger, SingletonLoggerConfig, SingletonLoggerBuilder
)
from .handlers import (
    HandlerBuilder, BaseHandlerConfig,
    EmailHandlerVersion1, EmailHandlerVersion1Config,
    StreamHandlerVersion1Config
)

