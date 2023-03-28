from typing import Optional, List, Tuple, Dict, Set
from objects import User, Post
from .base_general_recommender import (
    BaseGeneralRecommender, BaseGeneralRecommenderConfig
)
from utils.thread_utils import ThreadWithReturnValue
from repositories.readers import (
    BaseUserReader, BaseUserReaderConfig,
    BaseGeneralScoreReader, BaseGeneralScoreReaderConfig,
    BaseUserPostsReader, BaseUserPostsReaderConfig
)
from logger import SingletonLogger


class GeneralRecommenderVersion1(BaseGeneralRecommender):
    """
    Read user history + general score
    Remove post in user positive history
    Sort by score
    """
    def __init__(
            self, user_reader: Optional[BaseUserReader],
            general_score_reader: BaseGeneralScoreReader,
            user_excluded_posts_reader: Optional[BaseUserPostsReader]
    ):
        """
        Init method
        :param user_reader: read user history
        :param general_score_reader: read general score
        :param user_excluded_posts_reader: read posts excluded for recommend
        """
        super(GeneralRecommenderVersion1, self).__init__()
        self.user_reader = user_reader
        self.general_score_reader = general_score_reader
        self.user_excluded_posts_reader = user_excluded_posts_reader

    @property
    def user_reader(self) -> Optional[BaseUserReader]:
        return self._user_reader

    @user_reader.setter
    def user_reader(self, user_reader: Optional[BaseUserReader]):
        if user_reader is not None:
            assert isinstance(user_reader, BaseUserReader)
        self._user_reader: Optional[BaseUserReader] = user_reader

    @property
    def general_score_reader(self) -> BaseGeneralScoreReader:
        return self._general_score_reader

    @general_score_reader.setter
    def general_score_reader(self, general_score_reader: BaseGeneralScoreReader):
        assert isinstance(general_score_reader, BaseGeneralScoreReader)
        self._general_score_reader: BaseGeneralScoreReader = general_score_reader

    @property
    def user_excluded_posts_reader(self) -> Optional[BaseUserPostsReader]:
        return self._user_excluded_posts_reader

    @user_excluded_posts_reader.setter
    def user_excluded_posts_reader(self, user_excluded_posts_reader: Optional[BaseUserPostsReader]):
        if user_excluded_posts_reader is not None:
            assert isinstance(user_excluded_posts_reader, BaseUserPostsReader)
        self._user_excluded_posts_reader: Optional[BaseUserPostsReader] = user_excluded_posts_reader

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
        try:
            # read user history and general score
            if self.user_reader:
                thread_1 = ThreadWithReturnValue(
                    func=self.user_reader.read_user,
                    func_kwargs={"user": user}
                )
                thread_1.start()
                thread_2 = ThreadWithReturnValue(
                    func=self.general_score_reader.read
                )
                thread_2.start()
                thread_1.join()
                post_to_score: Optional[Dict[Post, float]] = thread_2.join()
            else:
                post_to_score: Optional[
                    Dict[Post, float]
                ] = self.general_score_reader.read()
            if not post_to_score:
                return None
            # filter valid posts and sort by score
            excluded_posts: Set[Post] = self._get_excluded_posts(user=user)
            included_posts_scores: List[
                Tuple[Post, float]
            ] = []
            excluded_posts_scores: List[
                Tuple[Post, float]
            ] = []
            for post, score in post_to_score.items():
                if post in excluded_posts:
                    excluded_posts_scores.append(
                        (post, score)
                    )
                else:
                    included_posts_scores.append(
                        (post, score)
                    )
            included_posts_scores: List[
                Tuple[Post, float]
            ] = sorted(
                included_posts_scores, key=lambda x: x[1], reverse=True
            )
            if len(included_posts_scores) >= limit:
                return included_posts_scores[:limit]
            excluded_posts_scores: List[
                Tuple[Post, float]
            ] = sorted(
                excluded_posts_scores, key=lambda x: x[1], reverse=True
            )
            return (
                included_posts_scores + excluded_posts_scores
            )[:limit]
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading get general recommend"
            )


class GeneralRecommenderVersion1Config(BaseGeneralRecommenderConfig):
    """
    Read user history + general score
    Remove post in user positive history
    Sort by score
    """
    def __init__(
            self, user_reader_config: Optional[BaseUserReaderConfig],
            general_score_reader_config: BaseGeneralScoreReaderConfig,
            user_excluded_posts_reader_config: Optional[BaseUserPostsReaderConfig]
    ):
        """
        Init method
        :param user_reader_config: read user history
        :param general_score_reader_config: read general score
        :param user_excluded_posts_reader_config: read excluded posts for recommend
        """
        super(GeneralRecommenderVersion1Config, self).__init__()
        self.user_reader_config = user_reader_config
        self.general_score_reader_config = general_score_reader_config
        self.user_excluded_posts_reader_config = user_excluded_posts_reader_config

    @property
    def user_reader_config(self) -> Optional[BaseUserReaderConfig]:
        return self._user_reader_config

    @user_reader_config.setter
    def user_reader_config(self, user_reader_config: Optional[BaseUserReaderConfig]):
        if user_reader_config is not None:
            assert isinstance(user_reader_config, BaseUserReaderConfig)
        self._user_reader_config: Optional[BaseUserReaderConfig] = user_reader_config

    @property
    def general_score_reader_config(self) -> BaseGeneralScoreReaderConfig:
        return self._general_score_reader_config

    @general_score_reader_config.setter
    def general_score_reader_config(self, general_score_reader_config: BaseGeneralScoreReaderConfig):
        assert isinstance(general_score_reader_config, BaseGeneralScoreReaderConfig)
        self._general_score_reader_config: BaseGeneralScoreReaderConfig = general_score_reader_config

    @property
    def user_excluded_posts_reader_config(self) -> Optional[BaseUserPostsReaderConfig]:
        return self._user_excluded_posts_reader_config

    @user_excluded_posts_reader_config.setter
    def user_excluded_posts_reader_config(self, user_excluded_posts_reader_config: Optional[BaseUserPostsReaderConfig]):
        if user_excluded_posts_reader_config is not None:
            assert isinstance(user_excluded_posts_reader_config, BaseUserPostsReaderConfig)
        self._user_excluded_posts_reader_config: Optional[BaseUserPostsReaderConfig] = user_excluded_posts_reader_config
