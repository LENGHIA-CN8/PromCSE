from .base_object_writer import (
    BaseObjectWriter, BaseObjectWriterConfig
)
from .pickle_object_writer_version_1 import (
    PickleObjectWriterVersion1, PickleObjectWriterVersion1Config
)
from .auto_retry_object_writer_version_1 import (
    AutoRetryObjectWriterVersion1, AutoRetryObjectWriterVersion1Config
)
from .chain_object_writer_version_1 import (
    ChainObjectWriterVersion1, ChainObjectWriterVersion1Config
)


class ObjectWriterBuilder:
    """
    Class for build object writer
    """
    @classmethod
    def build_object_writer(
            cls, config: BaseObjectWriterConfig
    ) -> BaseObjectWriter:
        if isinstance(config, PickleObjectWriterVersion1Config):
            return PickleObjectWriterVersion1(
                file_name=config.file_name
            )
        elif isinstance(config, ChainObjectWriterVersion1Config):
            return ChainObjectWriterVersion1(
                wrapped_writer=cls.build_object_writer(
                    config=config.wrapped_writer_config
                ),
                next_writer=cls.build_object_writer(
                    config=config.next_writer_config
                ) if config.next_writer_config is not None else None,
                time_break=config.time_break
            )
        elif isinstance(config, AutoRetryObjectWriterVersion1Config):
            return AutoRetryObjectWriterVersion1(
                wrapped_writer=cls.build_object_writer(
                    config=config.wrapped_writer_config
                ),
                num_tries=config.num_tries, time_break=config.time_break
            )
        else:
            raise ValueError(
                f"Invalid object writer class: {config}"
            )
