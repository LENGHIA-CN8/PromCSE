from typing import Optional, Tuple
from objects import Post
from .base_mysql_all_posts_reader_version_1 import (
    BaseMySQLAllPostsReaderVersion1,
    BaseMySQLAllPostsReaderVersion1Config
)
from connector_proxies import (
    BaseMySQLConnectorProxy, BaseMySQLConnectorProxyConfig
)
from datetime import datetime, timedelta


class MySQLAllPostsReaderVersion2(BaseMySQLAllPostsReaderVersion1):
    """
    Read posts from MySQL
    Only read posts from a source news
    Only read posts that were published in recent x hours
    Only read posts haven't been removed
    Only read postId
    """
    def __init__(
            self, connector: BaseMySQLConnectorProxy,
            source_news: str, hour_window: int
    ):
        """
        Init method
        :param connector: connection to database
        :param source_news: source news to read data
        :param hour_window: only read posts that were published in recent x hours
        """
        super(MySQLAllPostsReaderVersion2, self).__init__(
            connector=connector
        )
        self.source_news = source_news
        self.hour_window = hour_window

    @property
    def source_news(self) -> str:
        return self._source_news

    @source_news.setter
    def source_news(self, source_news: str):
        assert isinstance(source_news, str)
        self._source_news: str = source_news

    @property
    def hour_window(self) -> int:
        return self._hour_window

    @hour_window.setter
    def hour_window(self, hour_window: int):
        assert isinstance(hour_window, int)
        self._hour_window: int = hour_window

    def _get_sql_command(self) -> str:
        """
        Get sql command for query
        :return: sql command
        """
        threshold: datetime = datetime.now() - timedelta(
            hours=self.hour_window
        )
        return f"""
            SELECT newsId
            FROM news_resource
            WHERE sourceNews = "{self.source_news}"
            AND publishDate >= "{threshold.strftime('%Y-%m-%d %H:%M:%S')}"
        """

    def _get_post_from_tuple_data(
            self, data: Tuple
    ) -> Optional[Post]:
        """
        Get post from a tuple
        :param data: tuple data
        :return: post object if success, else None
        """
        if (
                len(data) != 1 or
                not isinstance(data[0], int)
        ):
            return None
        return Post(post_id=data[0])


class MySQLAllPostsReaderVersion2Config(BaseMySQLAllPostsReaderVersion1Config):
    """
    Config for read posts from MySQL
    Only read posts from a source news
    Only read posts that were published in recent x hours
    Only read posts haven't been removed
    Only read postId
    """
    def __init__(
            self, connector_config: BaseMySQLConnectorProxyConfig,
            source_news: str, hour_window: int
    ):
        """
        Init method
        :param connector_config: connection to database
        :param source_news: source news to read data
        :param hour_window: only read posts that were published in recent x hours
        """
        super(MySQLAllPostsReaderVersion2Config, self).__init__(
            connector_config=connector_config
        )
        self.source_news = source_news
        self.hour_window = hour_window

    @property
    def source_news(self) -> str:
        return self._source_news

    @source_news.setter
    def source_news(self, source_news: str):
        assert isinstance(source_news, str)
        self._source_news: str = source_news

    @property
    def hour_window(self) -> int:
        return self._hour_window

    @hour_window.setter
    def hour_window(self, hour_window: int):
        assert isinstance(hour_window, int)
        self._hour_window: int = hour_window
