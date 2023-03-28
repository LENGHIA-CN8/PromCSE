from .base_relate_score_reader import (
    BaseRelateScoreReader, BaseRelateScoreReaderConfig
)
from .hbase_relate_score_reader_version_1 import (
    HbaseRelateScoreReaderVersion1, HbaseRelateScoreReaderVersion1Config
)
from connector_proxies import (
    HbaseConnectorProxyFlyweight
)


class RelateScoreReaderBuilder:
    """
    Class for building relate score reader
    """
    @classmethod
    def build_relate_score_reader(
            cls, config: BaseRelateScoreReaderConfig
    ) -> BaseRelateScoreReader:
        if isinstance(
            config, HbaseRelateScoreReaderVersion1Config
        ):
            return HbaseRelateScoreReaderVersion1(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, column_name=config.column_name,
                batch_size=config.batch_size,
                verbose=config.verbose, stale_threshold=config.stale_threshold
            )
        else:
            raise ValueError(
                f"Invalid relate score reader class: {config}"
            )
