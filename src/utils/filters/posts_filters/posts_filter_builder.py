from .base_posts_filter import (
    BasePostsFilter, BasePostsFilterConfig
)
from .remove_duplicate_posts_filter_version_1 import (
    RemoveDuplicatePostsFilterVersion1,
    RemoveDuplicatePostsFilterVersion1Config
)
from .remove_missing_encodes_posts_filter_version_1 import (
    RemoveMissingEncodesPostsFilterVersion1,
    RemoveMissingEncodesPostsFilterVersion1Config
)
from .remove_mismatch_encodes_posts_filter_version_1 import (
    RemoveMismatchEncodesPostsFilterVersion1,
    RemoveMismatchEncodesPostsFilterVersion1Config
)
from .remove_missing_publish_date_posts_filter_version_1 import (
    RemoveMissingPublishDatePostsFilterVersion1,
    RemoveMissingPublishDatePostsFilterVersion1Config
)
from .remove_stale_posts_filter_version_1 import (
    RemoveOldPostsFilterVersion1,
    RemoveOldPostsFilterVersion1Config
)
from .chain_posts_filter_version_1 import (
    ChainPostsFilterVersion1, ChainPostsFilterVersion1Config
)


class PostsFilterBuilder:
    """
    Class for building posts filter
    """
    @classmethod
    def build_posts_filter(
            cls, config: BasePostsFilterConfig
    ) -> BasePostsFilter:
        if isinstance(config, RemoveDuplicatePostsFilterVersion1Config):
            return RemoveDuplicatePostsFilterVersion1(
                threshold=config.threshold
            )
        elif isinstance(config, RemoveMissingEncodesPostsFilterVersion1Config):
            return RemoveMissingEncodesPostsFilterVersion1(
                encode_names=config.encode_names
            )
        elif isinstance(config, RemoveMismatchEncodesPostsFilterVersion1Config):
            return RemoveMismatchEncodesPostsFilterVersion1(
                encode_names=config.encode_names
            )
        elif isinstance(config, RemoveMissingPublishDatePostsFilterVersion1Config):
            return RemoveMissingPublishDatePostsFilterVersion1()
        elif isinstance(config, RemoveOldPostsFilterVersion1Config):
            return RemoveOldPostsFilterVersion1(
                hour_window=config.hour_window
            )
        elif isinstance(config, ChainPostsFilterVersion1Config):
            return ChainPostsFilterVersion1(
                filters=[
                    cls.build_posts_filter(config=filter_config)
                    for filter_config in config.filters_config
                ]
            )
        else:
            raise ValueError(
                f"Invalid posts filter class: {config}"
            )
