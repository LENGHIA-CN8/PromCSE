from typing import List
from objects import Post
from .base_posts_handler import (
    BasePostsHandler, BasePostsHandlerConfig
)
from utils.filters import (
    BasePostsFilter, BasePostsFilterConfig
)


class OnFilterPostsHandlerVersion1(BasePostsHandler):
    """
    Handle on a filtered posts set
    """
    def __init__(
            self, posts_filter: BasePostsFilter,
            wrapped_handler: BasePostsHandler
    ):
        """
        Init method
        :param posts_filter: filter posts for handle
        :param wrapped_handler: handler
        """
        super(OnFilterPostsHandlerVersion1, self).__init__()
        self.posts_filter = posts_filter
        self.wrapped_handler = wrapped_handler

    @property
    def posts_filter(self) -> BasePostsFilter:
        return self._posts_filter

    @posts_filter.setter
    def posts_filter(self, posts_filter: BasePostsFilter):
        assert isinstance(posts_filter, BasePostsFilter)
        self._posts_filter: BasePostsFilter = posts_filter

    @property
    def wrapped_handler(self) -> BasePostsHandler:
        return self._wrapped_handler

    @wrapped_handler.setter
    def wrapped_handler(self, wrapped_handler: BasePostsHandler):
        assert isinstance(wrapped_handler, BasePostsHandler)
        self._wrapped_handler: BasePostsHandler = wrapped_handler

    def handle_posts(
            self, posts: List[Post]
    ):
        """
        Handle posts
        :param posts: created posts to handle
        """
        posts: List[Post] = self.posts_filter.filter_posts(
            posts=posts
        )
        if len(posts) > 0:
            self.wrapped_handler.handle_posts(posts=posts)


class OnFilterPostsHandlerVersion1Config(BasePostsHandlerConfig):
    """
    Config for handle on a filtered posts set
    """
    def __init__(
            self, posts_filter_config: BasePostsFilterConfig,
            wrapped_handler_config: BasePostsHandlerConfig
    ):
        """
        Init method
        :param posts_filter_config: filter posts for handle
        :param wrapped_handler_config: handler
        """
        super(OnFilterPostsHandlerVersion1Config, self).__init__()
        self.posts_filter_config = posts_filter_config
        self.wrapped_handler_config = wrapped_handler_config

    @property
    def posts_filter_config(self) -> BasePostsFilterConfig:
        return self._posts_filter_config

    @posts_filter_config.setter
    def posts_filter_config(self, posts_filter_config: BasePostsFilterConfig):
        assert isinstance(posts_filter_config, BasePostsFilterConfig)
        self._posts_filter_config: BasePostsFilterConfig = posts_filter_config

    @property
    def wrapped_handler_config(self) -> BasePostsHandlerConfig:
        return self._wrapped_handler_config

    @wrapped_handler_config.setter
    def wrapped_handler_config(self, wrapped_handler_config: BasePostsHandlerConfig):
        assert isinstance(wrapped_handler_config, BasePostsHandlerConfig)
        self._wrapped_handler_config: BasePostsHandlerConfig = wrapped_handler_config

