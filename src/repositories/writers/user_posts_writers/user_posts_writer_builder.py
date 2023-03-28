from .base_user_posts_writer import (
    BaseUserPostsWriterConfig, BaseUserPostsWriter
)
from .aerospike_user_posts_writer_version_1 import (
    AerospikeUserPostsWriterVersion1Config,
    AerospikeUserPostsWriterVersion1
)
from connector_proxies import (
    AerospikeConnectorProxyFlyweight
)


class UserPostsWriterBuilder:
    """
    Class for building posts writer
    """
    @classmethod
    def build_user_posts_writer(
            cls, config: BaseUserPostsWriterConfig
    ) -> BaseUserPostsWriter:
        if isinstance(
            config, AerospikeUserPostsWriterVersion1Config
        ):
            return AerospikeUserPostsWriterVersion1(
                connector=AerospikeConnectorProxyFlyweight.get_aerospike_connector_proxy(
                    config=config.connector_config
                ),
                ae_namespace=config.ae_namespace, ae_set=config.ae_set,
                time_to_live=config.time_to_live,
                stale_threshold=config.stale_threshold
            )
        else:
            raise ValueError(
                f"Invalid user posts writer class: {config}"
            )
