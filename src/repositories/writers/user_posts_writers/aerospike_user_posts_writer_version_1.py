from typing import List, Dict
from connector_proxies import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from objects import Post
from .base_aerospike_user_posts_writer_version_1 import (
    BaseAerospikeUserPostsWriterVersion1,
    BaseAerospikeUserPostsWriterVersion1Config
)
from datetime import datetime


class AerospikeUserPostsWriterVersion1(BaseAerospikeUserPostsWriterVersion1):
    """
    Class for writing user posts to Aerospike
    - data:
        [
            "post_id",
            "timestamp"
        ],
        [
            "post_id",
            "timestamp"
        ],
    """
    def __init__(
            self, connector: BaseAerospikeConnectorProxy,
            ae_namespace: str, ae_set: str,
            time_to_live: int, stale_threshold: int
    ):
        """
        Init method
        :param connector: connector to AE
        :param ae_namespace: name space store data
        :param ae_set: set store data
        :param time_to_live: time to persist data
        :param stale_threshold: threshold to remove record from bins
        """
        super(AerospikeUserPostsWriterVersion1, self).__init__(
            connector=connector, ae_namespace=ae_namespace,
            ae_set=ae_set, time_to_live=time_to_live
        )
        self.stale_threshold = stale_threshold

    @property
    def stale_threshold(self) -> int:
        return self._stale_threshold

    @stale_threshold.setter
    def stale_threshold(self, stale_threshold: int):
        assert isinstance(stale_threshold, int)
        self._stale_threshold: int = stale_threshold

    def _convert_posts_to_bins(
            self, posts: List[Post], old_bins: Dict
    ) -> Dict:
        """
        Convert posts to bins
        :param posts: posts to convert
        :param old_bins: old bins data in Ae
        :return: new bins data
        """
        current_timestamp: int = int(datetime.now().timestamp())
        new_bins: Dict = {
            "data": [
                {
                    "post_id": str(post.post_id),
                    "timestamp": str(current_timestamp)
                }
                for post in posts
            ]
        }
        if (
            "data" not in old_bins or
            not isinstance(old_bins["data"], list)
        ):
            return new_bins
        for instance in old_bins["data"]:
            if not isinstance(instance, dict):
                continue
            timestamp = instance.get("timestamp")
            if (
                not isinstance(timestamp, str) or
                not timestamp.isdigit()
            ):
                continue
            timestamp: int = int(timestamp)
            if current_timestamp - timestamp <= self.stale_threshold:
                new_bins["data"].append(instance)
        return new_bins


class AerospikeUserPostsWriterVersion1Config(BaseAerospikeUserPostsWriterVersion1Config):
    """
    config class for writing user posts to Aerospike
    """
    def __init__(
            self, connector_config: BaseAerospikeConnectorProxyConfig,
            ae_namespace: str, ae_set: str,
            time_to_live: int, stale_threshold: int
    ):
        """
        Init method
        :param connector_config: connector to AE
        :param ae_namespace: name space store data
        :param ae_set: set store data
        :param time_to_live: time to persist data
        :param stale_threshold: threshold to remove record from bins
        """
        super(AerospikeUserPostsWriterVersion1Config, self).__init__(
            connector_config=connector_config, ae_namespace=ae_namespace,
            ae_set=ae_set, time_to_live=time_to_live
        )
        self.stale_threshold = stale_threshold

    @property
    def stale_threshold(self) -> int:
        return self._stale_threshold

    @stale_threshold.setter
    def stale_threshold(self, stale_threshold: int):
        assert isinstance(stale_threshold, int)
        self._stale_threshold: int = stale_threshold
