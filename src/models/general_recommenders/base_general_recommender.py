from abc import ABC, abstractmethod
from objects import User, Post
from typing import List, Tuple, Optional


class BaseGeneralRecommender(ABC):
    """
    Base class from recommend general
    """
    @abstractmethod
    def recommend(
            self, user: User, limit: int
    ) -> Optional[
        List[Tuple[Post, float]]
    ]:
        """
        Recommend for users base on general reason (no per)
        :param user: user to recommend
        :param limit: number of recommend
        :return: list of (post, float) or None
        """
        pass


class BaseGeneralRecommenderConfig(ABC):
    """
    Base config class from recommend general
    """
    pass
