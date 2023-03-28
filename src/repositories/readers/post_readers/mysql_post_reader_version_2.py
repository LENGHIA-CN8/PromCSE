from typing import Tuple, Optional, List
from objects import Post
from .base_mysql_post_reader_version_1 import (
    BaseMySQLPostReaderVersion1, BaseMySQLPostReaderVersion1Config
)


class MySQLPostReaderVersion2(BaseMySQLPostReaderVersion1):
    """
    Read post tags from MySQL database
    Only read posts from a source news
    """
    def _get_sql_command_for_post(self, post: Post) -> str:
        """
        Get sql command corresponding to a post
        :param post: post to get sql command
        :return: sql command
        """
        return f"""
            SELECT newsId, tags
            FROM news_resource
            WHERE sourceNews = "{self.source_news}"
            AND newsId = {post.post_id}
        """

    def _get_sql_command_for_posts(self, posts: List[Post]) -> str:
        """
        Get sql command for collection of posts
        :param posts: posts to get sql command
        :return: sql command
        """
        param: str = ", ".join(
            [str(post.post_id) for post in posts]
        )
        return f"""
            SELECT newsId, tags
            FROM news_resource
            WHERE sourceNews = "{self.source_news}"
            AND newsId IN ({param})
        """

    def _get_post_from_tuple(
            self, data: Tuple
    ) -> Optional[Post]:
        """
        Get post object from data tuple
        :param data: data tuple
        :return: post object (if success) or None
        """
        if len(data) != 2:
            # invalid tuple length
            return None
        post_id, tags = data
        if not isinstance(post_id, int):
            # invalid post id
            return None
        return Post(
            post_id=post_id,
            tags=tags if isinstance(tags, str) else None
        )


class MySQLPostReaderVersion2Config(BaseMySQLPostReaderVersion1Config):
    """
    Config for read post tags from MySQL database
    Only read posts from a source news
    """
    pass
