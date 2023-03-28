from typing import Optional, List, Tuple, Set
from utils.thread_utils import ThreadWithReturnValue
from objects import Post, User
from .base_relate_recommender import (
    BaseRelateRecommender, BaseRelateRecommenderConfig
)
from models.per_recommenders import (
    BasePerRecommender, BasePerRecommenderConfig
)
from models.general_recommenders import (
    BaseGeneralRecommender, BaseGeneralRecommenderConfig
)
from logger import SingletonLogger
from repositories.readers import (
    BaseUserReader, BaseUserReaderConfig
)


class RelateRecommenderVersion2(BaseRelateRecommender):
    """
    Relate that combine relate with per
    """
    def __init__(
            self, relate_recommender: BaseRelateRecommender,
            per_recommender: BasePerRecommender,
            user_reader: Optional[BaseUserReader],
            backup_recommender: Optional[BaseGeneralRecommender]
    ):
        """
        Init method
        :param relate_recommender: relate recommend
        :param per_recommender: per recommend
        :param user_reader: read user info
        :param backup_recommender: read backup result
        """
        super(RelateRecommenderVersion2, self).__init__()
        self.relate_recommender = relate_recommender
        self.per_recommender = per_recommender
        self.user_reader = user_reader
        self.backup_recommender = backup_recommender

    @property
    def relate_recommender(self) -> BaseRelateRecommender:
        return self._relate_recommender

    @relate_recommender.setter
    def relate_recommender(self, relate_recommender: BaseRelateRecommender):
        assert isinstance(relate_recommender, BaseRelateRecommender)
        self._relate_recommender: BaseRelateRecommender = relate_recommender

    @property
    def per_recommender(self) -> BasePerRecommender:
        return self._per_recommender

    @per_recommender.setter
    def per_recommender(self, per_recommender: BasePerRecommender):
        assert isinstance(per_recommender, BasePerRecommender)
        self._per_recommender: BasePerRecommender = per_recommender

    @property
    def user_reader(self) -> Optional[BaseUserReader]:
        return self._user_reader

    @user_reader.setter
    def user_reader(self, user_reader: Optional[BaseUserReader]):
        if user_reader is not None:
            assert isinstance(user_reader, BaseUserReader)
        self._user_reader: Optional[BaseUserReader] = user_reader

    @property
    def backup_recommender(self) -> Optional[BaseGeneralRecommender]:
        return self._backup_recommender

    @backup_recommender.setter
    def backup_recommender(self, backup_recommender: Optional[BaseGeneralRecommender]):
        if backup_recommender is not None:
            assert isinstance(backup_recommender, BaseGeneralRecommender)
        self._backup_recommender: Optional[BaseGeneralRecommender] = backup_recommender

    def _get_num_per(self, iter_index: int) -> int:
        """
        Get number of per in the iter index
        :param iter_index: index of iter
        :return: number of per
        """
        if iter_index == 0:
            return 1
        elif iter_index == 1:
            return 2
        else:
            return 1

    def _get_num_relate(self, iter_index: int) -> int:
        """
        Get number of relate in the iter index
        :param iter_index: index of iter
        :return: number of per
        """
        if iter_index == 0:
            return 3
        else:
            return 1

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
        try:
            # read user info
            if self.user_reader:
                self.user_reader.read_user(user=user)
            # read relate, per result
            thread_1 = ThreadWithReturnValue(
                func=self.relate_recommender.recommend,
                func_kwargs={
                    "seed_post": seed_post,
                    "user": user,
                    "limit": limit
                }
            )
            thread_1.start()
            thread_2 = ThreadWithReturnValue(
                func=self.per_recommender.recommend,
                func_kwargs={
                    "user": user,
                    "limit": limit
                }
            )
            thread_2.start()
            relate_result: Optional[
                List[Tuple[Post, float]]
            ] = thread_1.join()
            per_result: Optional[
                List[Tuple[Post, float]]
            ] = thread_2.join()
            # check bound condition
            if (
                not relate_result and
                not per_result
            ):
                if self.backup_recommender:
                    return self.backup_recommender.recommend(
                        user=user, limit=limit
                    )
                else:
                    return None
            if not relate_result:
                return per_result
            if not per_result:
                return relate_result
            # combine result
            add_posts: Set[Post] = set()
            posts_scores: List[Tuple[Post, float]] = []
            current_idx: int = 0
            while (
                len(relate_result) > 0 or
                len(per_result) > 0
            ):
                # add relate
                num_relate: int = self._get_num_relate(iter_index=current_idx)
                for post, score in relate_result[:num_relate]:
                    if post not in add_posts:
                        add_posts.add(post)
                        posts_scores.append((post, score))
                relate_result = relate_result[num_relate:]
                # add per
                num_per: int = self._get_num_per(iter_index=current_idx)
                for post, score in per_result[:num_per]:
                    if post not in add_posts:
                        add_posts.add(post)
                        posts_scores.append((post, score))
                per_result = per_result[num_per:]
                # check condition
                if len(posts_scores) >= limit:
                    return posts_scores[:limit]
                current_idx += 1
            return posts_scores[:limit]
        except:
            SingletonLogger.get_instance().exception(
                "Exception while compute relate recommendation"
            )
            return None


class RelateRecommenderVersion2Config(BaseRelateRecommenderConfig):
    """
    Relate that combine relate with per
    """
    def __init__(
            self, relate_recommender_config: BaseRelateRecommenderConfig,
            per_recommender_config: BasePerRecommenderConfig,
            user_reader_config: Optional[BaseUserReaderConfig],
            backup_recommender_config: Optional[BaseGeneralRecommenderConfig]
    ):
        """
        Init method
        :param relate_recommender_config: relate recommend
        :param per_recommender_config: per recommend
        :param user_reader_config: read user info
        :param backup_recommender_config: read backup result
        """
        super(RelateRecommenderVersion2Config, self).__init__()
        self.relate_recommender_config = relate_recommender_config
        self.per_recommender_config = per_recommender_config
        self.user_reader_config = user_reader_config
        self.backup_recommender_config = backup_recommender_config

    @property
    def relate_recommender_config(self) -> BaseRelateRecommenderConfig:
        return self._relate_recommender_config

    @relate_recommender_config.setter
    def relate_recommender_config(self, relate_recommender_config: BaseRelateRecommenderConfig):
        assert isinstance(relate_recommender_config, BaseRelateRecommenderConfig)
        self._relate_recommender_config: BaseRelateRecommenderConfig = relate_recommender_config

    @property
    def per_recommender_config(self) -> BasePerRecommenderConfig:
        return self._per_recommender_config

    @per_recommender_config.setter
    def per_recommender_config(self, per_recommender_config: BasePerRecommenderConfig):
        assert isinstance(per_recommender_config, BasePerRecommenderConfig)
        self._per_recommender_config: BasePerRecommenderConfig = per_recommender_config

    @property
    def user_reader_config(self) -> BaseUserReaderConfig:
        return self._user_reader_config

    @user_reader_config.setter
    def user_reader_config(self, user_reader_config: BaseUserReaderConfig):
        assert isinstance(user_reader_config, BaseUserReaderConfig)
        self._user_reader_config: BaseUserReaderConfig = user_reader_config

    @property
    def backup_recommender_config(self) -> BaseGeneralRecommenderConfig:
        return self._backup_recommender_config

    @backup_recommender_config.setter
    def backup_recommender_config(self, backup_recommender_config: BaseGeneralRecommenderConfig):
        assert isinstance(backup_recommender_config, BaseGeneralRecommenderConfig)
        self._backup_recommender_config: BaseGeneralRecommenderConfig = backup_recommender_config
