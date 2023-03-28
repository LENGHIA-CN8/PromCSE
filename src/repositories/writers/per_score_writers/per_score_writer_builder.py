from .base_per_score_writer import (
    BasePerScoreWriter, BasePerScoreWriterConfig
)
from .auto_retry_per_score_writer_version_1 import (
    AutoRetryPerScoreWriterVersion1,
    AutoRetryPerScoreWriterVersion1Config
)
from .hbase_per_score_writer_version_1 import (
    HbasePerScoreWriterVersion1, HbasePerScoreWriterVersion1Config
)
from .hbase_per_score_writer_version_2 import (
    HbasePerScoreWriterVersion2, HbasePerScoreWriterVersion2Config
)
from connector_proxies import (
    HbaseConnectorProxyFlyweight
)


class PerScoreWriterBuilder:
    """
    Class for writing per score
    """
    @classmethod
    def build_per_score_writer(
            cls, config: BasePerScoreWriterConfig
    ) -> BasePerScoreWriter:
        if isinstance(config, HbasePerScoreWriterVersion1Config):
            return HbasePerScoreWriterVersion1(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, column=config.column,
                batch_size=config.batch_size, verbose=config.verbose
            )
        elif isinstance(config, HbasePerScoreWriterVersion2Config):
            return HbasePerScoreWriterVersion2(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, column=config.column,
                batch_size=config.batch_size, verbose=config.verbose
            )
        elif isinstance(config, AutoRetryPerScoreWriterVersion1Config):
            return AutoRetryPerScoreWriterVersion1(
                wrapped_writer=cls.build_per_score_writer(
                    config=config.wrapped_writer_config
                ),
                num_tries=config.num_tries, time_between=config.time_between
            )
        else:
            raise ValueError(
                f"Invalid per score writer class: {config}"
            )
