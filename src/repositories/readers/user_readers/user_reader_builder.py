from .base_user_reader import (
    BaseUserReader, BaseUserReaderConfig
)
from .hbase_user_reader_version_1 import (
    HbaseUserReaderVersion1, HbaseUserReaderVersion1Config
)
from connector_proxies import (
    HbaseConnectorProxyFlyweight
)


class UserReaderBuilder:
    """
    Class for building user reader
    """
    @classmethod
    def build_user_reader(
            cls, config: BaseUserReaderConfig
    ) -> BaseUserReader:
        if isinstance(
            config, HbaseUserReaderVersion1Config
        ):
            return HbaseUserReaderVersion1(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name,
                batch_size=config.batch_size,
                positive_column=config.positive_column,
                negative_column=config.negative_column,
                verbose=config.verbose
            )
        else:
            raise ValueError(
                f"Invalid user reader class: {config}"
            )
