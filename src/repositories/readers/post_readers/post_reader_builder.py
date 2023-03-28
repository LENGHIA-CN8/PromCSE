from .base_post_reader import (
    BasePostReader, BasePostReaderConfig
)
from .mysql_post_reader_version_1 import (
    MySQLPostReaderVersion1, MySQLPostReaderVersion1Config
)
from .mysql_post_reader_version_2 import (
    MySQLPostReaderVersion2, MySQLPostReaderVersion2Config
)
from .hbase_post_reader_version_1 import (
    HbasePostReaderVersion1, HbasePostReaderVersion1Config
)
from .hbase_post_reader_version_2 import (
    HbasePostReaderVersion2, HbasePostReaderVersion2Config
)
from .hbase_post_reader_version_3 import (
    HbasePostReaderVersion3, HbasePostReaderVersion3Config
)
from .chain_post_reader_version_1 import (
    ChainPostReaderVersion1, ChainPostReaderVersion1Config
)
from .api_post_reader_version_1 import (
    ApiPostReaderVersion1, ApiPostReaderVersion1Config
)
from .tags_check_and_read_post_reader_version_1 import (
    TagsCheckAndReadPostReaderVersion1,
    TagsCheckAndReadPostReaderVersion1Config
)
from connector_proxies import (
    MySQLConnectorProxyFlyweight,
    HbaseConnectorProxyFlyweight
)


class PostReaderBuilder:
    """
    Class for building post reader
    """
    @classmethod
    def build_post_reader(
            cls, config: BasePostReaderConfig
    ) -> BasePostReader:
        if isinstance(config, MySQLPostReaderVersion1Config):
            return MySQLPostReaderVersion1(
                connector=MySQLConnectorProxyFlyweight.get_mysql_connector_proxy(
                    config=config.connector_config
                ),
                source_news=config.source_news, batch_size=config.batch_size,
                verbose=config.verbose
            )
        elif isinstance(config, MySQLPostReaderVersion2Config):
            return MySQLPostReaderVersion2(
                connector=MySQLConnectorProxyFlyweight.get_mysql_connector_proxy(
                    config=config.connector_config
                ),
                source_news=config.source_news, batch_size=config.batch_size,
                verbose=config.verbose
            )
        elif isinstance(config, HbasePostReaderVersion1Config):
            return HbasePostReaderVersion1(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, batch_size=config.batch_size,
                verbose=config.verbose, encode_columns=config.encode_columns
            )
        elif isinstance(config, HbasePostReaderVersion2Config):
            return HbasePostReaderVersion2(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, batch_size=config.batch_size,
                verbose=config.verbose, tags_column=config.tags_column
            )
        elif isinstance(config, HbasePostReaderVersion3Config):
            return HbasePostReaderVersion3(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, batch_size=config.batch_size,
                verbose=config.verbose, ners_column=config.ners_column
            )
        elif isinstance(config, ChainPostReaderVersion1Config):
            return ChainPostReaderVersion1(
                wrapped_readers=[
                    cls.build_post_reader(config=read_config)
                    for read_config in config.wrapped_readers_config
                ]
            )
        elif isinstance(config, ApiPostReaderVersion1Config):
            return ApiPostReaderVersion1(
                source_news=config.source_news, url=config.url,
                num_days=config.num_days, batch_size=config.batch_size,
                verbose=config.verbose
            )
        elif isinstance(config, TagsCheckAndReadPostReaderVersion1Config):
            return TagsCheckAndReadPostReaderVersion1(
                wrapped_reader=cls.build_post_reader(
                    config=config.wrapped_reader_config
                )
            )
        else:
            raise ValueError(
                f"Invalid post reader class: {config}"
            )
