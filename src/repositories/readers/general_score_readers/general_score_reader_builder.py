from .base_general_score_reader import (
    BaseGeneralScoreReader, BaseGeneralScoreReaderConfig
)
from .aerospike_general_score_reader_version_1 import (
    AerospikeGeneralScoreReaderVersion1, AerospikeGeneralScoreReaderVersion1Config
)
from connector_proxies import (
    AerospikeConnectorProxyFlyweight
)


class GeneralScoreReaderBuilder:
    """
    Class for building general score reader
    """
    @classmethod
    def build_general_score_reader(
            cls, config: BaseGeneralScoreReaderConfig
    ) -> BaseGeneralScoreReader:
        if isinstance(
            config, AerospikeGeneralScoreReaderVersion1Config
        ):
            return AerospikeGeneralScoreReaderVersion1(
                connector=AerospikeConnectorProxyFlyweight.get_aerospike_connector_proxy(
                    config=config.connector_config,
                ),
                key=config.key
            )
        else:
            raise ValueError(
                f"Invalid general score reader: {config}"
            )

