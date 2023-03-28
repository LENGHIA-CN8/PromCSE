from typing import Dict
from objects import Post
from .base_aerospike_general_score_writer_version_1 import (
    BaseAerospikeGeneralScoreWriterVersion1,
    BaseAerospikeGeneralScoreWriterVersion1Config
)


class AerospikeGeneralScoreWriterVersion1(BaseAerospikeGeneralScoreWriterVersion1):
    """
    Class for writing general score to Aerospike
    """
    def _get_bins(self, post_to_score: Dict[Post, float]) -> Dict:
        """
        Get bins to save in Aerospike
        :param post_to_score: mapping from post to score
        :return: bins as dict
        """
        return {
            "data": [
                {
                    "post_id": str(post.post_id),
                    "score": score
                }
                for post, score in post_to_score.items()
            ]
        }


class AerospikeGeneralScoreWriterVersion1Config(BaseAerospikeGeneralScoreWriterVersion1Config):
    """
    Config class for writing general score to Aerospike
    """
    pass
