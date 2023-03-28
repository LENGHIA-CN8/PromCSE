from .base_general_score_writer import (
    BaseGeneralScoreWriter, BaseGeneralScoreWriterConfig
)
from .aerospike_general_score_writer_version_1 import (
    AerospikeGeneralScoreWriterVersion1,
    AerospikeGeneralScoreWriterVersion1Config
)
from connector_proxies import (
    AerospikeConnectorProxyFlyweight
)


class GeneralScoreWriterBuilder:
    """
    Class for building general score writer
    """
    @classmethod
    def build_general_score_writer(
            cls, config: BaseGeneralScoreWriterConfig
    ) -> BaseGeneralScoreWriter:
        if isinstance(
            config, AerospikeGeneralScoreWriterVersion1Config
        ):
            return AerospikeGeneralScoreWriterVersion1(
                connector=AerospikeConnectorProxyFlyweight.get_aerospike_connector_proxy(
                    config=config.connector_config
                ),
                key=config.key, time_to_live=config.time_to_live
            )
        else:
            raise ValueError(
                f"Invalid general score class: {config}"
            )
