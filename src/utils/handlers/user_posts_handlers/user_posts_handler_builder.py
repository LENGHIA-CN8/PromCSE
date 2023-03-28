from .base_user_posts_handler import (
    BaseUserPostsHandlerConfig,
    BaseUserPostsHandler
)
from .save_user_posts_handler_version_1 import (
    SaveUserPostsHandlerVersion1Config,
    SaveUserPostsHandlerVersion1
)
from repositories.writers import (
    UserPostsWriterBuilder
)


class UserPostsHandlerBuilder:
    """
    Class for building user posts handler
    """
    @classmethod
    def build_user_posts_handler(
            cls, config: BaseUserPostsHandlerConfig
    ) -> BaseUserPostsHandler:
        if isinstance(
            config, SaveUserPostsHandlerVersion1Config
        ):
            return SaveUserPostsHandlerVersion1(
                top_k=config.top_k,
                writer=UserPostsWriterBuilder.build_user_posts_writer(
                    config=config.writer_config
                )
            )
        else:
            raise ValueError(
                f"Invalid user posts handler class: {config}"
            )
