"""
This package contains classes for filter texts
"""

from .base_text_filter import (
    BaseTextFilter, BaseTextFilterConfig
)
from .base_element_wise_text_filter_version_1 import (
    BaseElementWiseTextFilterVersion1, BaseElementWiseTextFilterVersion1Config
)
from .text_filter_builder import (
    TextFilterBuilder
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

