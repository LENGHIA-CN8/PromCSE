"""
This packages contains classes for filter objects
"""


from .text_filters import (
    BaseTextFilter, BaseTextFilterConfig,
    BaseElementWiseTextFilterVersion1, BaseElementWiseTextFilterVersion1Config,
    TextFilterBuilder,
    ShortTextFilterVersion1, ShortTextFilterVersion1Config,
    ShortTextFilterVersion2, ShortTextFilterVersion2Config,
    RemoveDuplicateTextFilterVersion1, RemoveDuplicateTextFilterVersion1Config,
    KeepFrequentTextFilterVersion1, KeepFrequentTextFilterVersion1Config,
    PrefixBasedTextFilterVersion1, PrefixBasedTextFilterVersion1Config,
    ChainTextFilterVersion1, ChainTextFilterVersion1Config
)
from .posts_filters import (
    BasePostsFilter, BasePostsFilterConfig,
    BaseElementWisePostsFilter,
    BaseElementWisePostsFilterConfig,
    PostsFilterBuilder,
    RemoveDuplicatePostsFilterVersion1,
    RemoveDuplicatePostsFilterVersion1Config,
    RemoveMissingEncodesPostsFilterVersion1,
    RemoveMissingEncodesPostsFilterVersion1Config,
    RemoveMismatchEncodesPostsFilterVersion1,
    RemoveMismatchEncodesPostsFilterVersion1Config,
    RemoveMissingPublishDatePostsFilterVersion1,
    RemoveMissingPublishDatePostsFilterVersion1Config,
    RemoveOldPostsFilterVersion1,
    RemoveOldPostsFilterVersion1Config,
    ChainPostsFilterVersion1, ChainPostsFilterVersion1Config
)
