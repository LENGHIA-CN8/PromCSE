from typing import List
from objects import Post
from .base_posts_filter import (
    BasePostsFilter, BasePostsFilterConfig
)


class ChainPostsFilterVersion1(BasePostsFilter):
    """
    Connect between filters to make a chain of responsibilities
    """
    def __init__(
            self, filters: List[BasePostsFilter]
    ):
        """
        Init method
        :param filters: list of filters
        """
        super(ChainPostsFilterVersion1, self).__init__()
        self.filters = filters

    @property
    def filters(self) -> List[BasePostsFilter]:
        return self._filters

    @filters.setter
    def filters(self, filters: List[BasePostsFilter]):
        assert isinstance(filters, list)
        assert all(map(lambda x: isinstance(x, BasePostsFilter), filters))
        self._filters: List[BasePostsFilter] = filters

    def filter_posts(
            self, posts: List[Post]
    ) -> List[Post]:
        """
        Remove invalid posts
        :param posts: list of posts
        :return: list valid posts
        """
        for filter_node in self.filters:
            posts = filter_node.filter_posts(posts=posts)
        return posts


class ChainPostsFilterVersion1Config(BasePostsFilterConfig):
    """
    Connect between filters to make a chain of responsibilities
    """
    def __init__(
            self, filters_config: List[BasePostsFilterConfig]
    ):
        """
        Init method
        :param filters_config: list of filters
        """
        super(ChainPostsFilterVersion1Config, self).__init__()
        self.filters_config = filters_config

    @property
    def filters_config(self) -> List[BasePostsFilterConfig]:
        return self._filters_config

    @filters_config.setter
    def filters_config(self, filters_config: List[BasePostsFilterConfig]):
        assert isinstance(filters_config, list)
        assert all(map(lambda x: isinstance(x, BasePostsFilterConfig), filters_config))
        self._filters_config: List[BasePostsFilterConfig] = filters_config
