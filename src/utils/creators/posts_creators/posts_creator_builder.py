from .base_posts_creator import (
    BasePostsCreator, BasePostsCreatorConfig
)
from .posts_creator_version_1 import (
    PostsCreatorVersion1, PostsCreatorVersion1Config
)
from repositories.readers import (
    AllPostsReaderBuilder
)
from utils.processors import (
    PostProcessorBuilder
)
from utils.filters import (
    PostsFilterBuilder
)
from utils.handlers import (
    PostsHandlerBuilder
)


class PostsCreatorBuilder:
    """
    Class for building posts creator
    """
    @classmethod
    def build_posts_creator(
            cls, config: BasePostsCreatorConfig
    ) -> BasePostsCreator:
        if isinstance(config, PostsCreatorVersion1Config):
            return PostsCreatorVersion1(
                all_posts_reader=AllPostsReaderBuilder.build_all_posts_reader(
                    config=config.all_posts_reader_config
                ),
                post_processor=PostProcessorBuilder.build_post_processor(
                    config=config.post_processor_config
                ) if config.post_processor_config is not None else None,
                posts_filter=PostsFilterBuilder.build_posts_filter(
                    config=config.posts_filter_config
                ) if config.posts_filter_config is not None else None,
                posts_handler=PostsHandlerBuilder.build_posts_handler(
                    config=config.posts_handler_config
                ) if config.posts_handler_config is not None else None
            )
        else:
            raise ValueError(
                f"Invalid posts creator class: {config}"
            )
