from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from objects import Post


class BaseRelateScoreWriter(ABC):
    """
    Base class for writing relate score
    """
    @abstractmethod
    def write_score(
            self, seed_post: Post,
            posts_scores: List[Tuple[Post, float]]
    ) -> bool:
        """
        Write relate score
        :param seed_post: seed post
        :param posts_scores: list scores of candidates. list of tuple (post, score)
        :return: True if success, else False
        """
        pass

    @abstractmethod
    def write_scores(
            self, seed_post_to_result: Dict[
                Post,
                List[Tuple[Post, float]]
            ]
    ) -> bool:
        """
        Write multiple relate scores
        :param seed_post_to_result: mapping from seed post to list of tuple (post, score)
        :return True if success, else False
        """
        pass


class BaseRelateScoreWriterConfig(ABC):
    """
    Base config class for writing relate score
    """
    pass
