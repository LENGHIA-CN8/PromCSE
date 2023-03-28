from .base_posts_handler import (
    BasePostsHandler, BasePostsHandlerConfig
)
from .save_posts_handler_version_1 import (
    SavePostsHandlerVersion1, SavePostsHandlerVersion1Config
)
from .on_filter_posts_handler_version_1 import (
    OnFilterPostsHandlerVersion1, OnFilterPostsHandlerVersion1Config
)
from utils.filters import (
    PostsFilterBuilder
)
from repositories.writers import (
    PostWriterBuilder
)


class PostsHandlerBuilder:
    """
    Class for building posts handler
    """
    @classmethod
    def build_posts_handler(
            cls, config: BasePostsHandlerConfig
    ) -> BasePostsHandler:
        if isinstance(config, SavePostsHandlerVersion1Config):
            return SavePostsHandlerVersion1(
                writer=PostWriterBuilder.build_post_writer(
                    config=config.writer_config
                )
            )
        elif isinstance(config, OnFilterPostsHandlerVersion1Config):
            return OnFilterPostsHandlerVersion1(
                posts_filter=PostsFilterBuilder.build_posts_filter(
                    config=config.posts_filter_config
                ),
                wrapped_handler=cls.build_posts_handler(
                    config=config.wrapped_handler_config
                )
            )
        else:
            raise ValueError(
                f"Invalid posts handler class: {config}"
            )
