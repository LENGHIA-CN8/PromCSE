from logger import (
    SingletonLoggerBuilder, SingletonLoggerConfig,
    StreamHandlerVersion1Config
)
from models.per_recommenders import (
    BasePerRecommender, PerRecommenderBuilder,
    PerRecommenderVersion1Config
)
from models.relate_recommenders import (
    BaseRelateRecommender, RelateRecommenderBuilder,
    RelateRecommenderVersion1Config
)
from models.general_recommenders import (
    GeneralRecommenderVersion1Config
)
from repositories.readers import (
    HbaseUserReaderVersion1Config,
    AerospikeGeneralScoreReaderVersion1Config,
    AerospikeUserPostsReaderVersion1Config,
    BasePostReader, PostReaderBuilder,
    MySQLPostReaderVersion1Config,
    HbasePerScoreReaderVersion1Config,
    HbaseRelateScoreReaderVersion1Config
)
from repositories.writers import (
    AerospikeUserPostsWriterVersion1Config
)
from utils.handlers import (
    BaseUserPostsHandler, UserPostsHandlerBuilder,
    SaveUserPostsHandlerVersion1Config
)
from connector_proxies import (
    HbaseConnectorProxyVersion1Config,
    MySQLConnectorProxyVersion1Config,
    AerospikeConnectorProxyVersion1Config
)
from config import (
    SOURCE_NEWS,
    HBASE_SERVERS, HBASE_PORT, HBASE_PROTOCOL, HBASE_TRANSPORT,
    HBASE_TIMEOUT, HBASE_USER_TABLE, HBASE_POST_TABLE,
    HBASE_PER_ROBERTA_COLUMN, HBASE_RELATE_ROBERTA_COLUMN,
    AEROSPIKE_HOSTS, AEROSPIKE_POLICIES,
    MYSQL_USER, MYSQL_HOST, MYSQL_DATABASE, MYSQL_PASSWORD,
    AE_CTR_KEY, AE_NAMESPACE, AE_REC_RECOMMEND_SET
)
from fastapi import FastAPI
from objects import User, Post
from typing import List, Tuple, Optional


SingletonLoggerBuilder.build_singleton_logger(
    config=SingletonLoggerConfig(
        handlers_config=[
            StreamHandlerVersion1Config()
        ],
        logger_name="API"
    )
)


hbase_connector_config = HbaseConnectorProxyVersion1Config(
    servers=HBASE_SERVERS, port=HBASE_PORT, transport=HBASE_TRANSPORT,
    protocol=HBASE_PROTOCOL, timeout=HBASE_TIMEOUT, pool_size=5
)
aerospike_connector_config = AerospikeConnectorProxyVersion1Config(
    hosts=AEROSPIKE_HOSTS, policies=AEROSPIKE_POLICIES
)
mysql_connector_config = MySQLConnectorProxyVersion1Config(
    host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE, pool_size=1
)


user_reader_config = HbaseUserReaderVersion1Config(
    connector_config=hbase_connector_config,
    table_name=HBASE_USER_TABLE, batch_size=30,
    positive_column=b'cf:positive', negative_column=b'cf:negative',
    verbose=False
)
user_excluded_posts_reader_config = AerospikeUserPostsReaderVersion1Config(
    connector_config=aerospike_connector_config,
    ae_namespace=AE_NAMESPACE, ae_set=AE_REC_RECOMMEND_SET,
    stale_threshold=1*60*60, min_freq=3
)
post_reader: BasePostReader = PostReaderBuilder.build_post_reader(
    config=MySQLPostReaderVersion1Config(
        connector_config=mysql_connector_config,
        source_news=SOURCE_NEWS, batch_size=100, verbose=False
    )
)


backup_recommender_config = GeneralRecommenderVersion1Config(
    user_reader_config=None,
    general_score_reader_config=AerospikeGeneralScoreReaderVersion1Config(
        connector_config=aerospike_connector_config, key=AE_CTR_KEY
    ),
    user_excluded_posts_reader_config=user_excluded_posts_reader_config
)


per_recommender: BasePerRecommender = PerRecommenderBuilder.build_per_recommender(
    config=PerRecommenderVersion1Config(
        user_reader_config=user_reader_config,
        per_score_reader_config=HbasePerScoreReaderVersion1Config(
            connector_config=hbase_connector_config,
            table_name=HBASE_USER_TABLE, column_name=HBASE_PER_ROBERTA_COLUMN,
            batch_size=30, verbose=False, stale_threshold=3*24*60*60
        ),
        backup_recommender_config=backup_recommender_config,
        user_excluded_posts_reader_config=user_excluded_posts_reader_config
    )
)


relate_recommender: BaseRelateRecommender = RelateRecommenderBuilder.build_relate_recommender(
    config=RelateRecommenderVersion1Config(
        user_reader_config=user_reader_config,
        relate_score_reader_config=HbaseRelateScoreReaderVersion1Config(
            connector_config=hbase_connector_config,
            table_name=HBASE_POST_TABLE, column_name=HBASE_RELATE_ROBERTA_COLUMN,
            batch_size=30, verbose=False, stale_threshold=3*24*60*60
        ),
        backup_recommender_config=backup_recommender_config,
        user_excluded_posts_reader_config=user_excluded_posts_reader_config
    )
)


user_posts_handler: BaseUserPostsHandler = UserPostsHandlerBuilder.build_user_posts_handler(
    config=SaveUserPostsHandlerVersion1Config(
        top_k=6,
        writer_config=AerospikeUserPostsWriterVersion1Config(
            connector_config=aerospike_connector_config,
            ae_namespace=AE_NAMESPACE, ae_set=AE_REC_RECOMMEND_SET,
            time_to_live=1*60*60, stale_threshold=1*60*60
        )
    )
)


app = FastAPI()


@app.get("/")
async def ping():
    return "pong"


@app.get("/per")
async def per(user_id: int, limit: int = 6):
    user = User(user_id=user_id)
    # get recommend result
    posts_scores: Optional[
        List[Tuple[Post, float]]
    ] = per_recommender.recommend(user=user, limit=limit)
    # get format result
    if not posts_scores:
        return {
            "message": "Failed to get recommendation",
            "recommend": []
        }
    else:
        user_posts_handler.handle(
            user=user,
            posts=[post for post, _ in posts_scores]
        )
        return {
            "message": "Recommend successfully",
            "recommend": [
                {
                    "id": str(post.post_id),
                    "score": score
                }
                for post, score in posts_scores
            ]
        }


@app.get("/per_debug")
async def per_debug(user_id: int, limit: int = 6):
    user = User(user_id=user_id)
    # get recommend result
    posts_scores: Optional[
        List[Tuple[Post, float]]
    ] = per_recommender.recommend(user=user, limit=limit)
    # get format result
    if not posts_scores:
        return {
            "message": "Failed to get recommendation",
            "recommend": []
        }
    else:
        post_reader.read_posts(
            posts=[
                post for post, _ in posts_scores
            ] + user.positive_posts[:15]
        )
        return {
            "message": "Recommend successfully",
            "history": [
                {
                    "id": post.post_id,
                    "title": post.title,
                    "sapo": post.sapo
                }
                for post in user.positive_posts[:15] if post.title is not None
            ],
            "recommend": [
                {
                    "id": str(post.post_id),
                    "title": post.title,
                    "sapo": post.sapo,
                    "score": score
                }
                for post, score in posts_scores
            ]
        }


@app.get("/relate")
async def relate(
        user_id: int, seed_post_id: int, limit: int = 6
):
    user = User(user_id=user_id)
    seed_post = Post(post_id=seed_post_id)
    # get result
    posts_scores: Optional[
        List[Tuple[Post, float]]
    ] = relate_recommender.recommend(
        user=user, seed_post=seed_post, limit=limit
    )
    # get format result
    if not posts_scores:
        return {
            "message": "Failed to get recommendation",
            "recommend": []
        }
    else:
        user_posts_handler.handle(
            user=user,
            posts=[post for post, _ in posts_scores]
        )
        return {
            "message": "Recommend successfully",
            "recommend": [
                {
                    "id": str(post.post_id),
                    "score": score
                }
                for post, score in posts_scores
            ]
        }


@app.get("/relate_debug")
async def relate_debug(
        user_id: int, seed_post_id: int, limit: int = 6
):
    user = User(user_id=user_id)
    seed_post = Post(post_id=seed_post_id)
    # get result
    posts_scores: Optional[
        List[Tuple[Post, float]]
    ] = relate_recommender.recommend(
        user=user, seed_post=seed_post, limit=limit
    )
    # get format result
    if not posts_scores:
        return {
            "message": "Failed to get recommendation",
            "recommend": []
        }
    else:
        post_reader.read_posts(
            posts=[post for post, _ in posts_scores] + [seed_post]
        )
        return {
            "message": "Recommend successfully",
            "seed_post": {
                "id": str(seed_post.post_id),
                "title": seed_post.title,
                "sapo": seed_post.sapo,
            },
            "recommend": [
                {
                    "id": str(post.post_id),
                    "title": post.title,
                    "sapo": post.sapo,
                    "score": score
                }
                for post, score in posts_scores
            ]
        }
