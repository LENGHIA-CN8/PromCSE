from typing import Optional, List
from objects import Post
from .base_all_posts_reader import (
    BaseAllPostsReader, BaseAllPostsReaderConfig
)
from repositories.readers.post_readers import (
    BasePostReader, BasePostReaderConfig
)


class WithInfoAllPostsReaderVersion1(BaseAllPostsReader):
    """
    Reading all posts, and read additional info for posts
    """
    def __init__(
            self, all_posts_reader: BaseAllPostsReader,
            post_reader: BasePostReader
    ):
        """
        Init method
        :param all_posts_reader: read all posts
        :param post_reader: read post additional info
        """
        super(WithInfoAllPostsReaderVersion1, self).__init__()
        self.all_posts_reader = all_posts_reader
        self.post_reader = post_reader

    @property
    def all_posts_reader(self) -> BaseAllPostsReader:
        return self._all_posts_reader

    @all_posts_reader.setter
    def all_posts_reader(self, all_posts_reader: BaseAllPostsReader):
        assert isinstance(all_posts_reader, BaseAllPostsReader)
        self._all_posts_reader: BaseAllPostsReader = all_posts_reader

    @property
    def post_reader(self) -> BasePostReader:
        return self._post_reader

    @post_reader.setter
    def post_reader(self, post_reader: BasePostReader):
        assert isinstance(post_reader, BasePostReader)
        self._post_reader: BasePostReader = post_reader

    def read_posts(self) -> Optional[List[Post]]:
        """
        Read list of posts
        :return: list of posts, None if failed
        """
        posts: Optional[List[Post]] = self.all_posts_reader.read_posts()
        if posts is None:
            return None
        self.post_reader.read_posts(posts=posts)
        return posts


class WithInfoAllPostsReaderVersion1Config(BaseAllPostsReaderConfig):
    """
    Config for reading all posts, and read additional info for posts
    """
    def __init__(
            self, all_posts_reader_config: BaseAllPostsReaderConfig,
            post_reader_config: BasePostReaderConfig
    ):
        """
        Init method
        :param all_posts_reader_config: read all posts
        :param post_reader_config: read post additional info
        """
        super(WithInfoAllPostsReaderVersion1Config, self).__init__()
        self.all_posts_reader_config = all_posts_reader_config
        self.post_reader_config = post_reader_config

    @property
    def all_posts_reader_config(self) -> BaseAllPostsReaderConfig:
        return self._all_posts_reader_config

    @all_posts_reader_config.setter
    def all_posts_reader_config(self, all_posts_reader_config: BaseAllPostsReaderConfig):
        assert isinstance(all_posts_reader_config, BaseAllPostsReaderConfig)
        self._all_posts_reader_config: BaseAllPostsReaderConfig = all_posts_reader_config

    @property
    def post_reader_config(self) -> BasePostReaderConfig:
        return self._post_reader_config

    @post_reader_config.setter
    def post_reader_config(self, post_reader_config: BasePostReaderConfig):
        assert isinstance(post_reader_config, BasePostReaderConfig)
        self._post_reader_config: BasePostReaderConfig = post_reader_config
