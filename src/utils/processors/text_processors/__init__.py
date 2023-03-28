"""
This package contains classes for process text
"""


from .base_text_processor import (
    BaseTextProcessor, BaseTextProcessorConfig
)
from .base_element_wise_text_processor import (
    BaseElementWiseTextProcessor,
    BaseElementWiseTextProcessorConfig
)
from .text_processor_builder import (
    TextProcessorBuilder
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
