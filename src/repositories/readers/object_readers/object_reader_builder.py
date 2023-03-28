from .base_object_reader import (
    BaseObjectReader, BaseObjectReaderConfig
)
from .pickle_object_reader_version_1 import (
    PickleObjectReaderVersion1Config, PickleObjectReaderVersion1
)
from .auto_retry_object_reader_version_1 import (
    AutoRetryObjectReaderVersion1, AutoRetryObjectReaderVersion1Config
)
from .chain_object_reader_version_1 import (
    ChainObjectReaderVersion1, ChainObjectReaderVersion1Config
)


class ObjectReaderBuilder:
    """
    Class for building object reader
    """
    @classmethod
    def build_object_reader(
            cls, config: BaseObjectReaderConfig
    ) -> BaseObjectReader:
        if isinstance(config, PickleObjectReaderVersion1Config):
            return PickleObjectReaderVersion1(
                file_name=config.file_name
            )
        elif isinstance(config, ChainObjectReaderVersion1Config):
            return ChainObjectReaderVersion1(
                wrapped_reader=cls.build_object_reader(
                    config=config.wrapped_reader_config
                ),
                next_reader=cls.build_object_reader(
                    config=config.next_reader_config
                ) if config.next_reader_config is not None else None,
                time_break=config.time_break
            )
        elif isinstance(config, AutoRetryObjectReaderVersion1Config):
            return AutoRetryObjectReaderVersion1(
                wrapped_reader=cls.build_object_reader(
                    config=config.wrapped_reader_config
                ), num_tries=config.num_tries,
                time_break=config.time_break
            )
        else:
            raise ValueError(
                f"Invalid object reader class: {config}"
            )
