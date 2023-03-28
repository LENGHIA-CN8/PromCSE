from abc import ABC, abstractmethod
from objects import User, Post
from typing import List, Optional, Tuple


class BasePerRecommender(ABC):
    """
    Base class for personalized recommender
    """
    @abstractmethod
    def recommend(
            self, user: User, limit: int
    ) -> Optional[
        List[Tuple[Post, float]]
    ]:
        """
        Compute per recommend
        :param user: user
        :param limit: number of posts to return
        :return: list of (post, score)
        """
        pass


class BasePerRecommenderConfig(ABC):
    """
    Base config class for personalized recommender
    """
    pass

