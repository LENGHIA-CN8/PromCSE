from typing import List
from objects import Post
from .base_element_wise_posts_filter import (
    BaseElementWisePostsFilter,
    BaseElementWisePostsFilterConfig
)


class RemoveMissingEncodesPostsFilterVersion1(BaseElementWisePostsFilter):
    """
    Remove posts that missing any of specified encode
    """
    def __init__(
            self, encode_names: List[str]
    ):
        """
        Init method
        :param encode_names: list names of encodes to check
        """
        super(RemoveMissingEncodesPostsFilterVersion1, self).__init__()
        self.encode_names = encode_names

    @property
    def encode_names(self) -> List[str]:
        return self._encode_names

    @encode_names.setter
    def encode_names(self, encode_names: List[str]):
        assert isinstance(encode_names, list)
        assert all(map(lambda x: isinstance(x, str), encode_names))
        self._encode_names: List[str] = encode_names

    def _is_valid(self, post: Post) -> bool:
        """
        Check if post is valid
        :param post: post to check
        :return: True if valid, else False
        """
        for encode_name in self.encode_names:
            if post.get_encode(encode_name=encode_name) is None:
                return False
        return True


class RemoveMissingEncodesPostsFilterVersion1Config(BaseElementWisePostsFilterConfig):
    """
    Config for remove posts that missing any of specified encode
    """
    def __init__(
            self, encode_names: List[str]
    ):
        """
        Init method
        :param encode_names: list names of encodes to check
        """
        super(RemoveMissingEncodesPostsFilterVersion1Config, self).__init__()
        self.encode_names = encode_names

    @property
    def encode_names(self) -> List[str]:
        return self._encode_names

    @encode_names.setter
    def encode_names(self, encode_names: List[str]):
        assert isinstance(encode_names, list)
        assert all(map(lambda x: isinstance(x, str), encode_names))
        self._encode_names: List[str] = encode_names
