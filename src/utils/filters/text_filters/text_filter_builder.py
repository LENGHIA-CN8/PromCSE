from .base_text_filter import (
    BaseTextFilter, BaseTextFilterConfig
)
from .short_text_filter_version_1 import (
    ShortTextFilterVersion1, ShortTextFilterVersion1Config
)
from .short_text_filter_version_2 import (
    ShortTextFilterVersion2, ShortTextFilterVersion2Config
)
from .keep_frequent_text_filter_version_1 import (
    KeepFrequentTextFilterVersion1, KeepFrequentTextFilterVersion1Config
)
from .remove_duplicate_text_filter_version_1 import (
    RemoveDuplicateTextFilterVersion1, RemoveDuplicateTextFilterVersion1Config
)
from .prefix_based_text_filter_version_1 import (
    PrefixBasedTextFilterVersion1Config, PrefixBasedTextFilterVersion1
)
from .chain_text_filter_version_1 import (
    ChainTextFilterVersion1, ChainTextFilterVersion1Config
)


class TextFilterBuilder:
    """
    Class for building text filter
    """
    @classmethod
    def build_text_filter(
            cls, config: BaseTextFilterConfig
    ) -> BaseTextFilter:
        if isinstance(
            config, ShortTextFilterVersion1Config
        ):
            return ShortTextFilterVersion1(
                threshold=config.threshold,
                verbose=config.verbose
            )
        elif isinstance(
            config, ShortTextFilterVersion2Config
        ):
            return ShortTextFilterVersion2(
                threshold=config.threshold,
                verbose=config.verbose
            )
        elif isinstance(
            config, KeepFrequentTextFilterVersion1Config
        ):
            return KeepFrequentTextFilterVersion1(
                threshold=config.threshold
            )
        elif isinstance(
            config, RemoveDuplicateTextFilterVersion1Config
        ):
            return RemoveDuplicateTextFilterVersion1()
        elif isinstance(
            config, PrefixBasedTextFilterVersion1Config
        ):
            return PrefixBasedTextFilterVersion1(
                prefixes=config.prefixes, verbose=config.verbose
            )
        elif isinstance(
            config, ChainTextFilterVersion1Config
        ):
            return ChainTextFilterVersion1(
                filters=[
                    cls.build_text_filter(config=filter_config)
                    for filter_config in config.filters_config
                ]
            )
        else:
            raise ValueError(
                f"Invalid text filter class: {config}"
            )
