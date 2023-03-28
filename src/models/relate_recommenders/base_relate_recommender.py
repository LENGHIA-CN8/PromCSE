from abc import ABC, abstractmethod
from objects import User, Post
from typing import List, Optional, Tuple


class BaseRelateRecommender(ABC):
    """
    Base class for relate recommender
    """
    @abstractmethod
    def recommend(
            self, seed_post: Post, user: User, limit: int
    ) -> Optional[
        List[Tuple[Post, float]]
    ]:
        """
        Compute relate recommend
        :param seed_post: seed post to recommend
        :param user: user
        :param limit: number of posts to return
        :return: list of (post, score)
        """
        pass


class BaseRelateRecommenderConfig(ABC):
    """
    Base config class for relate recommender
    """
    pass

