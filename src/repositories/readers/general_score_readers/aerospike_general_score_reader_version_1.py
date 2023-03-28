from typing import Optional, Dict
from objects import Post
from .base_aerospike_general_score_reader_version_1 import (
    BaseAerospikeGeneralScoreReaderVersion1,
    BaseAerospikeGeneralScoreReaderVersion1Config
)


class AerospikeGeneralScoreReaderVersion1(BaseAerospikeGeneralScoreReaderVersion1):
    """
    Read general score from Aerospike
    """
    def _convert_bins_to_score(
            self, bins: Dict
    ) -> Optional[Dict[Post, float]]:
        """
        Convert AE bins to score
        :return: mapping from post to score, or None
        """
        if (
            "data" not in bins or
            not isinstance(bins["data"], list)
        ):
            return None
        post_to_score: Dict[Post, float] = {}
        for instance in bins["data"]:
            if (
                not isinstance(instance, dict) or
                "post_id" not in instance or
                "score" not in instance
            ):
                continue
            if (
                not isinstance(instance["post_id"], str) or
                not instance["post_id"].isdigit()
            ):
                continue
            if not isinstance(instance["score"], float):
                continue
            post_to_score[Post(
                post_id=int(instance["post_id"])
            )] = instance["score"]
        return post_to_score


class AerospikeGeneralScoreReaderVersion1Config(BaseAerospikeGeneralScoreReaderVersion1Config):
    """
    Config for read general score from Aerospike
    """
    pass
