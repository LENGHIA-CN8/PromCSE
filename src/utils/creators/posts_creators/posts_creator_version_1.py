from typing import Optional, List
from repositories.readers import (
    BaseAllPostsReader, BaseAllPostsReaderConfig
)
from utils.processors.post_processors import (
    BasePostProcessor, BasePostProcessorConfig
)
from utils.filters import (
    BasePostsFilter, BasePostsFilterConfig
)
from utils.handlers.posts_handlers import (
    BasePostsHandler, BasePostsHandlerConfig
)
from objects import Post
from .base_posts_creator import (
    BasePostsCreator, BasePostsCreatorConfig
)


class PostsCreatorVersion1(BasePostsCreator):
    """
    Workflow:
        - read all posts as posts
        - process posts (if needed)
        - filter posts (if needed)
        - handle posts (if needed)
    """
    def __init__(
            self, all_posts_reader: BaseAllPostsReader,
            post_processor: Optional[BasePostProcessor],
            posts_filter: Optional[BasePostsFilter],
            posts_handler: Optional[BasePostsHandler]
    ):
        """
        Init method
        :param all_posts_reader: read all posts as posts
        :param post_processor: process posts
        :param posts_filter: filter posts
        :param posts_handler: handle posts
        """
        super(PostsCreatorVersion1, self).__init__()
        self.all_posts_reader = all_posts_reader
        self.post_processor = post_processor
        self.posts_filter = posts_filter
        self.posts_handler = posts_handler

    @property
    def all_posts_reader(self) -> BaseAllPostsReader:
        return self._all_posts_reader

    @all_posts_reader.setter
    def all_posts_reader(self, all_posts_reader: BaseAllPostsReader):
        assert isinstance(all_posts_reader, BaseAllPostsReader)
        self._all_posts_reader: BaseAllPostsReader = all_posts_reader

    @property
    def post_processor(self) -> Optional[BasePostProcessor]:
        return self._post_processor

    @post_processor.setter
    def post_processor(self, post_processor: Optional[BasePostProcessor]):
        if post_processor is not None:
            assert isinstance(post_processor, BasePostProcessor)
        self._post_processor: Optional[BasePostProcessor] = post_processor

    @property
    def posts_filter(self) -> Optional[BasePostsFilter]:
        return self._posts_filter

    @posts_filter.setter
    def posts_filter(self, posts_filter: Optional[BasePostsFilter]):
        if posts_filter is not None:
            assert isinstance(posts_filter, BasePostsFilter)
        self._posts_filter: Optional[BasePostsFilter] = posts_filter

    @property
    def posts_handler(self) -> Optional[BasePostsHandler]:
        return self._posts_handler

    @posts_handler.setter
    def posts_handler(self, posts_handler: Optional[BasePostsHandler]):
        if posts_handler is not None:
            assert isinstance(posts_handler, BasePostsHandler)
        self._posts_handler: Optional[BasePostsHandler] = posts_handler

    def create_posts(self) -> Optional[List[Post]]:
        """
        Create posts
        :return: list of posts, or None if failed
        """
        posts: Optional[List[Post]] = self.all_posts_reader.read_posts()
        if not posts:
            return None
        if self.post_processor:
            self.post_processor.process_posts(posts=posts)
        if self.posts_filter:
            posts: List[Post] = self.posts_filter.filter_posts(
                posts=posts
            )
            if not posts:
                return None
        if self.posts_handler:
            self.posts_handler.handle_posts(
                posts=posts
            )
        return posts


class PostsCreatorVersion1Config(BasePostsCreatorConfig):
    """
    Workflow:
        - read all posts as posts
        - process posts (if needed)
        - filter posts (if needed)
        - handle posts (if needed)
    """
    def __init__(
            self, all_posts_reader_config: BaseAllPostsReaderConfig,
            post_processor_config: Optional[BasePostProcessorConfig],
            posts_filter_config: Optional[BasePostsFilterConfig],
            posts_handler_config: Optional[BasePostsHandlerConfig]
    ):
        """
        Init method
        :param all_posts_reader_config: read all posts as posts
        :param post_processor_config: process posts
        :param posts_filter_config: filter posts
        :param posts_handler_config: handle posts
        """
        super(PostsCreatorVersion1Config, self).__init__()
        self.all_posts_reader_config = all_posts_reader_config
        self.post_processor_config = post_processor_config
        self.posts_filter_config = posts_filter_config
        self.posts_handler_config = posts_handler_config

    @property
    def all_posts_reader_config(self) -> BaseAllPostsReaderConfig:
        return self._all_posts_reader_config

    @all_posts_reader_config.setter
    def all_posts_reader_config(self, all_posts_reader_config: BaseAllPostsReaderConfig):
        assert isinstance(all_posts_reader_config, BaseAllPostsReaderConfig)
        self._all_posts_reader_config: BaseAllPostsReaderConfig = all_posts_reader_config

    @property
    def post_processor_config(self) -> Optional[BasePostProcessorConfig]:
        return self._post_processor_config

    @post_processor_config.setter
    def post_processor_config(self, post_processor_config: Optional[BasePostProcessorConfig]):
        if post_processor_config is not None:
            assert isinstance(post_processor_config, BasePostProcessorConfig)
        self._post_processor_config: Optional[BasePostProcessorConfig] = post_processor_config

    @property
    def posts_filter_config(self) -> Optional[BasePostsFilterConfig]:
        return self._posts_filter_config

    @posts_filter_config.setter
    def posts_filter_config(self, posts_filter_config: Optional[BasePostsFilterConfig]):
        if posts_filter_config is not None:
            assert isinstance(posts_filter_config, BasePostsFilterConfig)
        self._posts_filter_config: Optional[BasePostsFilterConfig] = posts_filter_config

    @property
    def posts_handler_config(self) -> Optional[BasePostsHandlerConfig]:
        return self._posts_handler_config

    @posts_handler_config.setter
    def posts_handler_config(self, posts_handler_config: Optional[BasePostsHandlerConfig]):
        if posts_handler_config is not None:
            assert isinstance(posts_handler_config, BasePostsHandlerConfig)
        self._posts_handler_config: Optional[BasePostsHandlerConfig] = posts_handler_config
