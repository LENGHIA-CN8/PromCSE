from .base_aerospike_user_posts_reader_version_1 import (
    BaseAerospikeUserPostsReaderVersion1,
    BaseAerospikeUserPostsReaderVersion1Config
)
from typing import Optional, List, Dict
from objects import Post
from connector_proxies import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from datetime import datetime


class AerospikeUserPostsReaderVersion1(BaseAerospikeUserPostsReaderVersion1):
    """
    Base class for reading user posts from Ae
    """
    def __init__(
            self, connector: BaseAerospikeConnectorProxy,
            ae_namespace: str, ae_set: str,
            stale_threshold: int, min_freq: int
    ):
        """
        Init method
        :param connector: connector to AE
        :param ae_namespace: name space store data
        :param ae_set: set store data
        :param stale_threshold: only read records created in recent x seconds
        :param min_freq: only get posts appear more than x times
        """
        super(AerospikeUserPostsReaderVersion1, self).__init__(
            connector=connector, ae_namespace=ae_namespace,
            ae_set=ae_set
        )
        self.stale_threshold = stale_threshold
        self.min_freq = min_freq

    @property
    def stale_threshold(self) -> int:
        return self._stale_threshold

    @stale_threshold.setter
    def stale_threshold(self, stale_threshold: int):
        assert isinstance(stale_threshold, int)
        self._stale_threshold: int = stale_threshold

    @property
    def min_freq(self) -> int:
        return self._min_freq

    @min_freq.setter
    def min_freq(self, min_freq: int):
        assert isinstance(min_freq, int)
        self._min_freq: int = min_freq

    def _convert_bins_to_posts(
            self, bins: Dict
    ) -> Optional[List[Post]]:
        """
        Convert bins to list posts
        :param bins: ae bins
        :return: list of posts or None
        """
        if (
            "data" not in bins or
            not isinstance(bins["data"], list)
        ):
            return None
        current_timestamp: int = int(datetime.now().timestamp())
        post_id_to_count: Dict[int, int] = {}
        for instance in bins["data"]:
            if not isinstance(instance, dict):
                continue
            post_id = instance.get("post_id")
            timestamp = instance.get("timestamp")
            if (
                not isinstance(post_id, str) or
                not post_id.isdigit() or
                not isinstance(timestamp, str) or
                not timestamp.isdigit()
            ):
                continue
            post_id: int = int(post_id)
            timestamp: int = int(timestamp)
            if current_timestamp - timestamp <= self.stale_threshold:
                post_id_to_count[post_id] = post_id_to_count.get(post_id, 0) + 1
        return [
            Post(post_id=post_id)
            for post_id, count in post_id_to_count.items()
            if count >= self.min_freq
        ]


class AerospikeUserPostsReaderVersion1Config(BaseAerospikeUserPostsReaderVersion1Config):
    """
    Base class for reading user posts from Ae
    """
    def __init__(
            self, connector_config: BaseAerospikeConnectorProxyConfig,
            ae_namespace: str, ae_set: str,
            stale_threshold: int, min_freq: int
    ):
        """
        Init method
        :param connector_config: connector to AE
        :param ae_namespace: name space store data
        :param ae_set: set store data
        :param stale_threshold: only read records created in recent x seconds
        :param min_freq: only get posts appear more than x times
        """
        super(AerospikeUserPostsReaderVersion1Config, self).__init__(
            connector_config=connector_config,
            ae_namespace=ae_namespace, ae_set=ae_set
        )
        self.stale_threshold = stale_threshold
        self.min_freq = min_freq

    @property
    def stale_threshold(self) -> int:
        return self._stale_threshold

    @stale_threshold.setter
    def stale_threshold(self, stale_threshold: int):
        assert isinstance(stale_threshold, int)
        self._stale_threshold: int = stale_threshold

    @property
    def min_freq(self) -> int:
        return self._min_freq

    @min_freq.setter
    def min_freq(self, min_freq: int):
        assert isinstance(min_freq, int)
        self._min_freq: int = min_freq
