from .base_general_recommender import (
    BaseGeneralRecommender, BaseGeneralRecommenderConfig
)
from .general_recommender_version_1 import (
    GeneralRecommenderVersion1Config, GeneralRecommenderVersion1
)
from repositories.readers import (
    UserReaderBuilder, GeneralScoreReaderBuilder,
    UserPostsReaderBuilder
)


class GeneralRecommenderBuilder:
    """
    Class for building general recommender
    """
    @classmethod
    def build_general_recommender(
            cls, config: BaseGeneralRecommenderConfig
    ) -> BaseGeneralRecommender:
        if isinstance(
            config, GeneralRecommenderVersion1Config
        ):
            return GeneralRecommenderVersion1(
                user_reader=UserReaderBuilder.build_user_reader(
                    config=config.user_reader_config
                ) if config.user_reader_config is not None else None,
                general_score_reader=GeneralScoreReaderBuilder.build_general_score_reader(
                    config=config.general_score_reader_config
                ),
                user_excluded_posts_reader=UserPostsReaderBuilder.build_user_posts_reader(
                    config=config.user_excluded_posts_reader_config
                ) if config.user_excluded_posts_reader_config is not None else None
            )
        else:
            raise ValueError(
                f"Invalid general recommender class: {config}"
            )
