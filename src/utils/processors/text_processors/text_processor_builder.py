from .base_text_processor import (
    BaseTextProcessor, BaseTextProcessorConfig
)
from .lower_text_processor_version_1 import (
    LowerTextProcessorVersion1,
    LowerTextProcessorVersion1Config
)
from .remove_punctuation_text_processor_version_1 import (
    RemovePunctuationTextProcessorVersion1,
    RemovePunctuationTextProcessorVersion1Config
)
from .chain_text_processor_version_1 import (
    ChainTextProcessorVersion1,
    ChainTextProcessorVersion1Config
)
from .keep_alpha_text_processor_version_1 import (
    KeepAlphaTextProcessorVersion1,
    KeepAlphaTextProcessorVersion1Config
)
from .remove_html_text_processor_version_1 import (
    RemoveHtmlTextProcessorVersion1,
    RemoveHtmlTextProcessorVersion1Config
)
from .remove_duplicate_spaces_text_processor_version_1 import (
    RemoveDuplicateSpacesTextProcessorVersion1,
    RemoveDuplicateSpacesTextProcessorVersion1Config
)
from .tokenize_text_processor_version_1 import (
    TokenizeTextProcessorVersion1,
    TokenizeTextProcessorVersion1Config
)
from .tokenize_text_processor_version_2 import (
    TokenizeTextProcessorVersion2,
    TokenizeTextProcessorVersion2Config
)


class TextProcessorBuilder:
    """
    Class for building text processor
    """
    @classmethod
    def build_text_processor(
            cls, config: BaseTextProcessorConfig
    ) -> BaseTextProcessor:
        if isinstance(config, LowerTextProcessorVersion1Config):
            return LowerTextProcessorVersion1(
                verbose=config.verbose
            )
        elif isinstance(config, RemovePunctuationTextProcessorVersion1Config):
            return RemovePunctuationTextProcessorVersion1(
                verbose=config.verbose
            )
        elif isinstance(config, ChainTextProcessorVersion1Config):
            return ChainTextProcessorVersion1(
                processors=[
                    cls.build_text_processor(
                        config=processor_config
                    ) for processor_config in config.processors_config
                ],
                verbose=config.verbose
            )
        elif isinstance(config, KeepAlphaTextProcessorVersion1Config):
            return KeepAlphaTextProcessorVersion1(
                verbose=config.verbose
            )
        elif isinstance(config, RemoveHtmlTextProcessorVersion1Config):
            return RemoveHtmlTextProcessorVersion1(
                verbose=config.verbose
            )
        elif isinstance(config, RemoveDuplicateSpacesTextProcessorVersion1Config):
            return RemoveDuplicateSpacesTextProcessorVersion1(
                verbose=config.verbose
            )
        elif isinstance(config, TokenizeTextProcessorVersion1Config):
            return TokenizeTextProcessorVersion1(
                verbose=config.verbose
            )
        elif isinstance(config, TokenizeTextProcessorVersion2Config):
            return TokenizeTextProcessorVersion2(
                vn_core_address=config.vn_core_address,
                vn_core_port=config.vn_core_port,
                verbose=config.verbose
            )
        else:
            raise ValueError(
                f"Invalid text processor class: {config}"
            )
