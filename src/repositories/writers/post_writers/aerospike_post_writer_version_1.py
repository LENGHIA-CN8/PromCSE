from objects import Post
from .base_aerospike_post_writer_version_1 import (
    BaseAerospikePostWriterVersion1,
    BaseAerospikePostWriterVersion1Config
)
from typing import List, Dict


class AerospikePostWriterVersion1(BaseAerospikePostWriterVersion1):
    """
    Write posts to Aerospike
    All posts will be saved in a pre-defined key
    Only save post ids
    """
    def _get_bins(self, posts: List[Post]) -> Dict:
        """
        Get bins to save in Aerospike
        :param posts: list posts
        :return: bins as dict
        """
        return {
            "post_ids": [
                str(post.post_id) for post in posts
            ]
        }


class AerospikePostWriterVersion1Config(BaseAerospikePostWriterVersion1Config):
    """
    Write posts to Aerospike
    All posts will be saved in a pre-defined key
    Only save post ids
    """
    pass
