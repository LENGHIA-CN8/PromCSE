from .base_relate_recommender import (
    BaseRelateRecommender, BaseRelateRecommenderConfig
)
from .relate_recommender_version_1 import (
    RelateRecommenderVersion1, RelateRecommenderVersion1Config
)
from .relate_recommender_version_2 import (
    RelateRecommenderVersion2, RelateRecommenderVersion2Config
)
from repositories.readers import (
    UserReaderBuilder,
    RelateScoreReaderBuilder,
    UserPostsReaderBuilder,
)
from models.general_recommenders import (
    GeneralRecommenderBuilder
)
from models.per_recommenders import (
    PerRecommenderBuilder
)


class RelateRecommenderBuilder:
    """
    Class for building relate recommender
    """
    @classmethod
    def build_relate_recommender(
            cls, config: BaseRelateRecommenderConfig
    ) -> BaseRelateRecommender:
        if isinstance(
            config, RelateRecommenderVersion1Config
        ):
            return RelateRecommenderVersion1(
                user_reader=UserReaderBuilder.build_user_reader(
                    config=config.user_reader_config
                ) if config.user_reader_config is not None else None,
                relate_score_reader=RelateScoreReaderBuilder.build_relate_score_reader(
                    config=config.relate_score_reader_config
                ),
                user_excluded_posts_reader=UserPostsReaderBuilder.build_user_posts_reader(
                    config=config.user_excluded_posts_reader_config
                ) if config.user_excluded_posts_reader_config is not None else None,
                backup_recommender=GeneralRecommenderBuilder.build_general_recommender(
                    config=config.backup_recommender_config
                ) if config.backup_recommender_config is not None else None
            )
        elif isinstance(
            config, RelateRecommenderVersion2Config
        ):
            return RelateRecommenderVersion2(
                user_reader=UserReaderBuilder.build_user_reader(
                    config=config.user_reader_config
                ) if config.user_reader_config is not None else None,
                per_recommender=PerRecommenderBuilder.build_per_recommender(
                    config=config.per_recommender_config
                ),
                relate_recommender=cls.build_relate_recommender(
                    config=config.relate_recommender_config
                ),
                backup_recommender=GeneralRecommenderBuilder.build_general_recommender(
                    config=config.backup_recommender_config
                ) if config.backup_recommender_config is not None else None
            )
        else:
            raise ValueError(
                f"Invalid relate recommender class: {config}"
            )
