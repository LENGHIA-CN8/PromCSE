from objects import Post
from .base_element_wise_posts_filter import (
    BaseElementWisePostsFilter,
    BaseElementWisePostsFilterConfig
)


class RemoveMissingPublishDatePostsFilterVersion1(BaseElementWisePostsFilter):
    """
    Remove posts that missing publish date
    """

    def _is_valid(self, post: Post) -> bool:
        """
        Check if post is valid
        :param post: post to check
        :return: True if valid, else False
        """
        if post.publish_date is not None:
            return True
        else:
            return False


class RemoveMissingPublishDatePostsFilterVersion1Config(BaseElementWisePostsFilterConfig):
    """
    Config for remove posts that missing publish date
    """
    pass
