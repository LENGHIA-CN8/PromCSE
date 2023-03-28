from .base_all_posts_reader import (
    BaseAllPostsReader, BaseAllPostsReaderConfig
)
from .mysql_all_posts_reader_version_1 import (
    MySQLAllPostsReaderVersion1,
    MySQLAllPostsReaderVersion1Config
)
from .mysql_all_posts_reader_version_2 import (
    MySQLAllPostsReaderVersion2,
    MySQLAllPostsReaderVersion2Config
)
from .with_info_all_posts_reader_version_1 import (
    WithInfoAllPostsReaderVersion1,
    WithInfoAllPostsReaderVersion1Config
)
from repositories.readers.post_readers import (
    PostReaderBuilder
)
from connector_proxies import MySQLConnectorProxyFlyweight


class AllPostsReaderBuilder:
    """
    Class for building all posts reader
    """
    @classmethod
    def build_all_posts_reader(
            cls, config: BaseAllPostsReaderConfig
    ) -> BaseAllPostsReader:
        if isinstance(config, MySQLAllPostsReaderVersion1Config):
            return MySQLAllPostsReaderVersion1(
                connector=MySQLConnectorProxyFlyweight.get_mysql_connector_proxy(
                    config=config.connector_config
                ),
                source_news=config.source_news,
                hour_window=config.hour_window
            )
        elif isinstance(config, MySQLAllPostsReaderVersion2Config):
            return MySQLAllPostsReaderVersion2(
                connector=MySQLConnectorProxyFlyweight.get_mysql_connector_proxy(
                    config=config.connector_config
                ),
                source_news=config.source_news,
                hour_window=config.hour_window
            )
        elif isinstance(config, WithInfoAllPostsReaderVersion1Config):
            return WithInfoAllPostsReaderVersion1(
                all_posts_reader=cls.build_all_posts_reader(
                    config=config.all_posts_reader_config
                ),
                post_reader=PostReaderBuilder.build_post_reader(
                    config=config.post_reader_config
                )
            )
        else:
            raise ValueError(
                f"Invalid all posts reader class: {config}"
            )
