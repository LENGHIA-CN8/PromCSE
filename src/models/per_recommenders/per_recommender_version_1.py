from typing import Optional, List, Tuple, Set
from logger import SingletonLogger
from objects import User, Post
from .base_per_recommender import (
    BasePerRecommender, BasePerRecommenderConfig
)
from repositories.readers import (
    BasePerScoreReader, BasePerScoreReaderConfig,
    BaseUserReader, BaseUserReaderConfig,
    BaseUserPostsReader, BaseUserPostsReaderConfig
)
from utils.thread_utils import ThreadWithReturnValue
from models.general_recommenders import (
    BaseGeneralRecommender, BaseGeneralRecommenderConfig
)


class PerRecommenderVersion1(BasePerRecommender):
    """
    Workflow
        - read user history
        - read per recommend
        - if not have per recommend => read backup
        - sorting, remove posts from history + other excluded posts
    """
    def __init__(
            self, user_reader: Optional[BaseUserReader],
            per_score_reader: BasePerScoreReader,
            user_excluded_posts_reader: Optional[BaseUserPostsReader],
            backup_recommender: Optional[BaseGeneralRecommender]
    ):
        """
        Init method
        :param user_reader: read user history
        :param per_score_reader: read per score
        :param user_excluded_posts_reader: read posts excluded for recommend
        :param backup_recommender: backup recommender
        """
        super(PerRecommenderVersion1, self).__init__()
        self.user_reader = user_reader
        self.per_score_reader = per_score_reader
        self.user_excluded_posts_reader = user_excluded_posts_reader
        self.backup_recommender = backup_recommender

    @property
    def user_reader(self) -> Optional[BaseUserReader]:
        return self._user_reader

    @user_reader.setter
    def user_reader(self, user_reader: Optional[BaseUserReader]):
        if user_reader is not None:
            assert isinstance(user_reader, BaseUserReader)
        self._user_reader: Optional[BaseUserReader] = user_reader

    @property
    def per_score_reader(self) -> BasePerScoreReader:
        return self._per_score_reader

    @per_score_reader.setter
    def per_score_reader(self, per_score_reader: BasePerScoreReader):
        assert isinstance(per_score_reader, BasePerScoreReader)
        self._per_score_reader: BasePerScoreReader = per_score_reader

    @property
    def user_excluded_posts_reader(self) -> Optional[BaseUserPostsReader]:
        return self._user_excluded_posts_reader

    @user_excluded_posts_reader.setter
    def user_excluded_posts_reader(self, user_excluded_posts_reader: Optional[BaseUserPostsReader]):
        if user_excluded_posts_reader is not None:
            assert isinstance(user_excluded_posts_reader, BaseUserPostsReader)
        self._user_excluded_posts_reader: Optional[BaseUserPostsReader] = user_excluded_posts_reader

    @property
    def backup_recommender(self) -> Optional[BaseGeneralRecommender]:
        return self._backup_recommender

    @backup_recommender.setter
    def backup_recommender(self, backup_recommender: Optional[BaseGeneralRecommender]):
        if backup_recommender is not None:
            assert isinstance(backup_recommender, BaseGeneralRecommender)
        self._backup_recommender: Optional[BaseGeneralRecommender] = backup_recommender

    def _get_excluded_posts(self, user: User) -> Set[Post]:
        """
        Get set of excluded posts for recommend
        :param user: user to read
        :return: set of posts excluded for recommend
        """
        if self.user_excluded_posts_reader:
            excluded_posts: Optional[
                List[Post]
            ] = self.user_excluded_posts_reader.read_user(user=user)
        else:
            excluded_posts = None
        if excluded_posts:
            excluded_posts: Set[Post] = set(
                user.positive_posts + excluded_posts
            )
        else:
            excluded_posts: Set[Post] = set(user.positive_posts)
        return excluded_posts

    def recommend(self, user: User, limit: int) -> Optional[
        List[Tuple[Post, float]]
    ]:
        """
        Compute per recommend
        :param user: user
        :param limit: number of posts to return
        :return: list of (post, score)
        """
        try:
            # read user history, cached posts scores
            if self.user_reader:
                thread_1 = ThreadWithReturnValue(
                    func=self.user_reader.read_user,
                    func_kwargs={"user": user}
                )
                thread_1.start()
                thread_2 = ThreadWithReturnValue(
                    func=self.per_score_reader.read_user,
                    func_kwargs={"user": user}
                )
                thread_2.start()
                thread_1.join()
                posts_scores: Optional[
                    List[Tuple[Post, float]]
                ] = thread_2.join()
            else:
                posts_scores: Optional[
                    List[Tuple[Post, float]]
                ] = self.per_score_reader.read_user(user=user)
            # no per recommends
            if not posts_scores:
                if self.backup_recommender:
                    return self.backup_recommender.recommend(
                        user=user, limit=limit
                    )
                else:
                    return None
            # filter valid posts and sort by score
            excluded_posts: Set[Post] = self._get_excluded_posts(user=user)
            first_posts_scores: List[
                Tuple[Post, float]
            ] = []  # included posts
            second_posts_scores: List[
                Tuple[Post, float]
            ] = []  # excluded posts
            for post, score in posts_scores:
                if post in excluded_posts:
                    second_posts_scores.append(
                        (post, score)
                    )
                else:
                    first_posts_scores.append(
                        (post, score)
                    )
            first_posts_scores: List[
                Tuple[Post, float]
            ] = sorted(
                first_posts_scores, key=lambda x: x[1], reverse=True
            )
            if len(first_posts_scores) >= limit:
                return first_posts_scores[:limit]
            second_posts_scores: List[
                Tuple[Post, float]
            ] = sorted(
                second_posts_scores, key=lambda x: x[1], reverse=True
            )
            return (
                   first_posts_scores + second_posts_scores
            )[:limit]
        except:
            SingletonLogger.get_instance().exception(
                "Exception while recommend personalized posts"
            )
            return None


class PerRecommenderVersion1Config(BasePerRecommenderConfig):
    """
    Workflow
        - read user history
        - read per recommend
        - if not have per recommend => read backup
        - sorting, remove posts from history + other excluded posts
    """
    def __init__(
            self, user_reader_config: Optional[BaseUserReaderConfig],
            per_score_reader_config: BasePerScoreReaderConfig,
            user_excluded_posts_reader_config: Optional[BaseUserPostsReaderConfig],
            backup_recommender_config: Optional[BaseGeneralRecommenderConfig]
    ):
        """
        Init method
        :param user_reader_config: read user history
        :param per_score_reader_config: read per score
        :param user_excluded_posts_reader_config: read posts excluded for recommend
        :param backup_recommender_config: backup recommender
        """
        super(PerRecommenderVersion1Config, self).__init__()
        self.user_reader_config = user_reader_config
        self.per_score_reader_config = per_score_reader_config
        self.user_excluded_posts_reader_config = user_excluded_posts_reader_config
        self.backup_recommender_config = backup_recommender_config

    @property
    def user_reader_config(self) -> Optional[BaseUserReaderConfig]:
        return self._user_reader_config

    @user_reader_config.setter
    def user_reader_config(self, user_reader_config: Optional[BaseUserReaderConfig]):
        if user_reader_config is not None:
            assert isinstance(user_reader_config, BaseUserReaderConfig)
        self._user_reader_config: Optional[BaseUserReaderConfig] = user_reader_config

    @property
    def per_score_reader_config(self) -> BasePerScoreReaderConfig:
        return self._per_score_reader_config

    @per_score_reader_config.setter
    def per_score_reader_config(self, per_score_reader_config: BasePerScoreReaderConfig):
        assert isinstance(per_score_reader_config, BasePerScoreReaderConfig)
        self._per_score_reader_config: BasePerScoreReaderConfig = per_score_reader_config

    @property
    def user_excluded_posts_reader_config(self) -> Optional[BaseUserPostsReaderConfig]:
        return self._user_excluded_posts_reader_config

    @user_excluded_posts_reader_config.setter
    def user_excluded_posts_reader_config(self, user_excluded_posts_reader_config: Optional[BaseUserPostsReaderConfig]):
        if user_excluded_posts_reader_config is not None:
            assert isinstance(user_excluded_posts_reader_config, BaseUserPostsReaderConfig)
        self._user_excluded_posts_reader_config: Optional[BaseUserPostsReaderConfig] = user_excluded_posts_reader_config

    @property
    def backup_recommender_config(self) -> Optional[BaseGeneralRecommenderConfig]:
        return self._backup_recommender_config

    @backup_recommender_config.setter
    def backup_recommender_config(self, backup_recommender_config: Optional[BaseGeneralRecommenderConfig]):
        if backup_recommender_config is not None:
            assert isinstance(backup_recommender_config, BaseGeneralRecommenderConfig)
        self._backup_recommender_config: Optional[BaseGeneralRecommenderConfig] = backup_recommender_config
