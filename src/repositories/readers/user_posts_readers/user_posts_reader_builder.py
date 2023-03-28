from .base_user_posts_reader import (
    BaseUserPostsReader, BaseUserPostsReaderConfig
)
from .aerospike_user_posts_reader_version_1 import (
    AerospikeUserPostsReaderVersion1, AerospikeUserPostsReaderVersion1Config
)
from .hbase_user_posts_reader_version_1 import (
    HbaseUserPostsReaderVersion1, HbaseUserPostsReaderVersion1Config
)
from .chain_user_posts_reader_version_1 import (
    ChainUserPostsReaderVersion1, ChainUserPostsReaderVersion1Config
)
from connector_proxies import (
    AerospikeConnectorProxyFlyweight,
    HbaseConnectorProxyFlyweight
)


class UserPostsReaderBuilder:
    """
    Class for building user posts reader
    """
    @classmethod
    def build_user_posts_reader(
            cls, config: BaseUserPostsReaderConfig
    ) -> BaseUserPostsReader:
        if isinstance(
            config, AerospikeUserPostsReaderVersion1Config
        ):
            return AerospikeUserPostsReaderVersion1(
                connector=AerospikeConnectorProxyFlyweight.get_aerospike_connector_proxy(
                    config=config.connector_config
                ),
                ae_namespace=config.ae_namespace, ae_set=config.ae_set,
                stale_threshold=config.stale_threshold,
                min_freq=config.min_freq
            )
        elif isinstance(
            config, HbaseUserPostsReaderVersion1Config
        ):
            return HbaseUserPostsReaderVersion1(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, column=config.column
            )
        elif isinstance(
            config, ChainUserPostsReaderVersion1Config
        ):
            return ChainUserPostsReaderVersion1(
                readers=[
                    cls.build_user_posts_reader(
                        config=reader_config
                    )
                    for reader_config in config.readers_config
                ]
            )
        else:
            raise ValueError(
                f"Invalid user posts reader class:{config}"
            )
