from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from objects import Post, User


class BasePerScoreWriter(ABC):
    """
    Base class for writing per score
    """
    @abstractmethod
    def write_score(
            self, user: User,
            posts_scores: List[Tuple[Post, float]]
    ) -> bool:
        """
        Write per score
        :param user: user
        :param posts_scores: list scores of candidates. list of tuple (post, score)
        :return: True if success, else False
        """
        pass

    @abstractmethod
    def write_scores(
            self, user_to_result: Dict[
                User,
                List[Tuple[Post, float]]
            ]
    ) -> bool:
        """
        Write multiple per scores
        :param user_to_result: mapping from user to list of tuple (post, score)
        :return True if success, else False
        """
        pass


class BasePerScoreWriterConfig(ABC):
    """
    Base config class for writing per score
    """
    pass
