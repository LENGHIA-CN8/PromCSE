from .base_per_recommender import (
    BasePerRecommender, BasePerRecommenderConfig
)
from .per_recommender_version_1 import (
    PerRecommenderVersion1, PerRecommenderVersion1Config
)
from repositories.readers import (
    UserReaderBuilder,
    PerScoreReaderBuilder,
    UserPostsReaderBuilder,
)
from models.general_recommenders import (
    GeneralRecommenderBuilder
)


class PerRecommenderBuilder:
    """
    Class for building per recommender
    """
    @classmethod
    def build_per_recommender(
            cls, config: BasePerRecommenderConfig
    ) -> BasePerRecommender:
        if isinstance(
            config, PerRecommenderVersion1Config
        ):
            return PerRecommenderVersion1(
                user_reader=UserReaderBuilder.build_user_reader(
                    config=config.user_reader_config
                ) if config.user_reader_config is not None else None,
                per_score_reader=PerScoreReaderBuilder.build_per_score_reader(
                    config=config.per_score_reader_config
                ),
                user_excluded_posts_reader=UserPostsReaderBuilder.build_user_posts_reader(
                    config=config.user_excluded_posts_reader_config
                ) if config.user_excluded_posts_reader_config is not None else None,
                backup_recommender=GeneralRecommenderBuilder.build_general_recommender(
                    config=config.backup_recommender_config
                ) if config.backup_recommender_config is not None else None
            )
        else:
            raise ValueError(
                f"Invalid per recommender class: {config}"
            )
