from .base_relate_score_writer import (
    BaseRelateScoreWriter, BaseRelateScoreWriterConfig
)
from .auto_retry_relate_score_writer_version_1 import (
    AutoRetryRelateScoreWriterVersion1,
    AutoRetryRelateScoreWriterVersion1Config
)
from .hbase_relate_score_writer_version_1 import (
    HbaseRelateScoreWriterVersion1, HbaseRelateScoreWriterVersion1Config
)
from .hbase_relate_score_writer_version_2 import (
    HbaseRelateScoreWriterVersion2, HbaseRelateScoreWriterVersion2Config
)
from connector_proxies import (
    HbaseConnectorProxyFlyweight
)


class RelateScoreWriterBuilder:
    """
    Class for writing relate score
    """
    @classmethod
    def build_relate_score_writer(
            cls, config: BaseRelateScoreWriterConfig
    ) -> BaseRelateScoreWriter:
        if isinstance(config, HbaseRelateScoreWriterVersion1Config):
            return HbaseRelateScoreWriterVersion1(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, column=config.column,
                batch_size=config.batch_size, verbose=config.verbose
            )
        elif isinstance(config, HbaseRelateScoreWriterVersion2Config):
            return HbaseRelateScoreWriterVersion2(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, column=config.column,
                batch_size=config.batch_size, verbose=config.verbose
            )
        elif isinstance(config, AutoRetryRelateScoreWriterVersion1Config):
            return AutoRetryRelateScoreWriterVersion1(
                wrapped_writer=cls.build_relate_score_writer(
                    config=config.wrapped_writer_config
                ),
                num_tries=config.num_tries, time_between=config.time_between
            )
        else:
            raise ValueError(
                f"Invalid relate score writer class: {config}"
            )
