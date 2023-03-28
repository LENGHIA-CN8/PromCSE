from .base_post_writer import (
    BasePostWriter, BasePostWriterConfig
)
from .aerospike_post_writer_version_1 import (
    AerospikePostWriterVersion1,
    AerospikePostWriterVersion1Config
)
from .hbase_post_writer_version_1 import (
    HbasePostWriterVersion1, HbasePostWriterVersion1Config
)
from .hbase_post_writer_version_2 import (
    HbasePostWriterVersion2, HbasePostWriterVersion2Config
)
from .hbase_post_writer_version_3 import (
    HbasePostWriterVersion3, HbasePostWriterVersion3Config
)
from .auto_retry_post_writer_version_1 import (
    AutoRetryPostWriterVersion1, AutoRetryPostsWriterVersion1Config
)
from .chain_post_writer_version_1 import (
    ChainPostWriterVersion1, ChainPostWriterVersion1Config
)
from connector_proxies import (
    HbaseConnectorProxyFlyweight,
    AerospikeConnectorProxyFlyweight
)


class PostWriterBuilder:
    """
    Class for building post writer
    """
    @classmethod
    def build_post_writer(
            cls, config: BasePostWriterConfig
    ) -> BasePostWriter:
        if isinstance(config, AerospikePostWriterVersion1Config):
            return AerospikePostWriterVersion1(
                connector=AerospikeConnectorProxyFlyweight.get_aerospike_connector_proxy(
                    config=config.connector_config
                ),
                key=config.key, time_to_live=config.time_to_live
            )
        elif isinstance(config, HbasePostWriterVersion1Config):
            return HbasePostWriterVersion1(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, batch_size=config.batch_size,
                encode_name_to_column=config.encode_name_to_column,
                verbose=config.verbose
            )
        elif isinstance(config, HbasePostWriterVersion2Config):
            return HbasePostWriterVersion2(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, batch_size=config.batch_size,
                tags_column=config.tags_column,
                verbose=config.verbose
            )
        elif isinstance(config, HbasePostWriterVersion3Config):
            return HbasePostWriterVersion3(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, batch_size=config.batch_size,
                ners_column=config.ners_column,
                verbose=config.verbose
            )
        elif isinstance(config, AutoRetryPostsWriterVersion1Config):
            return AutoRetryPostWriterVersion1(
                wrapped_writer=cls.build_post_writer(
                    config=config.wrapped_writer_config
                ),
                num_tries=config.num_tries, time_between=config.time_between
            )
        elif isinstance(config, ChainPostWriterVersion1Config):
            return ChainPostWriterVersion1(
                writers=[
                    cls.build_post_writer(config=writer_config)
                    for writer_config in config.writers_config
                ]
            )
        else:
            raise ValueError(
                f"Invalid post writer class: {config}"
            )
