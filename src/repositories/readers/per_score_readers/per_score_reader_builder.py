from .base_per_score_reader import (
    BasePerScoreReader, BasePerScoreReaderConfig
)
from .hbase_per_score_reader_version_1 import (
    HbasePerScoreReaderVersion1, HbasePerScoreReaderVersion1Config
)
from connector_proxies import (
    HbaseConnectorProxyFlyweight
)


class PerScoreReaderBuilder:
    """
    Class for building per score reader
    """
    @classmethod
    def build_per_score_reader(
            cls, config: BasePerScoreReaderConfig
    ) -> BasePerScoreReader:
        if isinstance(
            config, HbasePerScoreReaderVersion1Config
        ):
            return HbasePerScoreReaderVersion1(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name, column_name=config.column_name,
                batch_size=config.batch_size,
                verbose=config.verbose, stale_threshold=config.stale_threshold
            )
        else:
            raise ValueError(
                f"Invalid per score reader class: {config}"
            )
