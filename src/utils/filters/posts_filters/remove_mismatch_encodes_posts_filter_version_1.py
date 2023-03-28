from typing import List, Dict, Set
from objects import Post
from .base_posts_filter import (
    BasePostsFilter, BasePostsFilterConfig
)


class RemoveMismatchEncodesPostsFilterVersion1(BasePostsFilter):
    """
    Remove all posts if they do not have same encodes timestamp
    """
    def __init__(
            self, encode_names: List[str]
    ):
        """
        Init method
        :param encode_names: list names of encodes to check
        """
        super(RemoveMismatchEncodesPostsFilterVersion1, self).__init__()
        self.encode_names = encode_names

    @property
    def encode_names(self) -> List[str]:
        return self._encode_names

    @encode_names.setter
    def encode_names(self, encode_names: List[str]):
        assert isinstance(encode_names, list)
        assert all(map(lambda x: isinstance(x, str), encode_names))
        self._encode_names: List[str] = encode_names

    def filter_posts(
            self, posts: List[Post]
    ) -> List[Post]:
        """
        Remove invalid posts
        :param posts: list of posts
        :return: list valid posts
        """
        encode_name_to_timestamps: Dict[str, Set[int]] = {
            encode_name: set() for encode_name in self.encode_names
        }
        for post in posts:
            for encode_name in self.encode_names:
                if post.get_encode(
                    encode_name=encode_name
                ) is not None:
                    encode_name_to_timestamps[encode_name].add(
                        post.get_encode(encode_name=encode_name).timestamp
                    )
        for encode_name, timestamps in encode_name_to_timestamps.items():
            if len(timestamps) > 1:
                return []
        return posts


class RemoveMismatchEncodesPostsFilterVersion1Config(BasePostsFilterConfig):
    """
    Config for remove all posts if they do not have same encodes timestamp
    """
    def __init__(
            self, encode_names: List[str]
    ):
        """
        Init method
        :param encode_names: list names of encodes to check
        """
        super(RemoveMismatchEncodesPostsFilterVersion1Config, self).__init__()
        self.encode_names = encode_names

    @property
    def encode_names(self) -> List[str]:
        return self._encode_names

    @encode_names.setter
    def encode_names(self, encode_names: List[str]):
        assert isinstance(encode_names, list)
        assert all(map(lambda x: isinstance(x, str), encode_names))
        self._encode_names: List[str] = encode_names
