from objects import Post
from .base_element_wise_posts_filter import (
    BaseElementWisePostsFilter,
    BaseElementWisePostsFilterConfig
)
from datetime import datetime, timedelta


class RemoveOldPostsFilterVersion1(BaseElementWisePostsFilter):
    """
    Remove too old posts
    """
    def __init__(
            self, hour_window: int
    ):
        """
        Init method
        :param hour_window: only kept posts created within x hours
        """
        super(RemoveOldPostsFilterVersion1, self).__init__()
        self.hour_window = hour_window

    @property
    def hour_window(self) -> int:
        return self._hour_window

    @hour_window.setter
    def hour_window(self, hour_window: int):
        assert isinstance(hour_window, int)
        self._hour_window: int = hour_window

    def _is_valid(self, post: Post) -> bool:
        """
        Check if post is valid
        :param post: post to check
        :return: True if valid, else False
        """
        if post.publish_date is None:
            return False
        threshold: datetime = datetime.now() - timedelta(
            hours=self.hour_window
        )
        return post.publish_date >= threshold


class RemoveOldPostsFilterVersion1Config(BaseElementWisePostsFilterConfig):
    """
    Remove too old posts
    """
    def __init__(
            self, hour_window: int
    ):
        """
        Init method
        :param hour_window: only kept posts created within x hours
        """
        super(RemoveOldPostsFilterVersion1Config, self).__init__()
        self.hour_window = hour_window

    @property
    def hour_window(self) -> int:
        return self._hour_window

    @hour_window.setter
    def hour_window(self, hour_window: int):
        assert isinstance(hour_window, int)
        self._hour_window: int = hour_window
