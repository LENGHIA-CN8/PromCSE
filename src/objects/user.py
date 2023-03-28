from .post import Post
from typing import List, Optional, Iterable, Dict
from collections import OrderedDict
from .encode import Encode


class User:
    """
    Class represent an user object
    """
    def __init__(
            self, user_id: int,
            positive_posts: Optional[List[Post]] = None,
            negative_posts: Optional[List[Post]] = None,
            encode: Optional[Encode] = None, encodes: Optional[Iterable[Encode]] = None
    ):
        """
        Init method
        :param user_id: id of user
        :param positive_posts: list of positive interacted posts
        :param negative_posts: list of negative interacted posts
        :param encode: encode
        :param encodes: collect of encode
        """
        self._positive_posts: OrderedDict[Post, Post] = OrderedDict()
        self._negative_posts: OrderedDict[Post, Post] = OrderedDict()
        self.__encode_name_to_encode: Dict[str, Encode] = {}
        self.user_id = user_id
        if positive_posts:
            self.add_positive_posts(posts=positive_posts)
        if negative_posts:
            self.add_negative_posts(posts=negative_posts)
        if encode is not None:
            self.add_encode(encode=encode)
        if encodes is not None:
            self.add_encodes(encodes=encodes)

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int):
        assert isinstance(user_id, int)
        self._user_id: int = user_id

    @property
    def positive_posts(self) -> List[Post]:
        return list(self._positive_posts.keys())

    @property
    def negative_posts(self) -> List[Post]:
        return list(self._negative_posts.keys())

    def add_positive_posts(
            self, posts: List[Post]
    ):
        """
        Add list posts to positive history
        :param posts: list of posts to add
        """
        assert isinstance(posts, list)
        assert all(map(lambda x: isinstance(x, Post), posts))
        for post in posts:
            if post not in self._positive_posts:
                self._positive_posts[post] = post

    def add_negative_posts(
            self, posts: List[Post]
    ):
        """
        Add list posts to negative history
        :param posts: list of posts to add
        """
        assert isinstance(posts, list)
        assert all(map(lambda x: isinstance(x, Post), posts))
        for post in posts:
            if post not in self._negative_posts:
                self._negative_posts[post] = post

    def add_encode(self, encode: Encode):
        """
        Add encode for post
        :param encode: encode object
        :return:
        """
        assert isinstance(encode, Encode)
        self.__encode_name_to_encode[encode.encode_name] = encode

    def add_encodes(self, encodes: Iterable[Encode]):
        """
        Add collection of encodes for post
        :param encodes: collection of encodes
        :return:
        """
        assert isinstance(encodes, Iterable)
        for encode in encodes:
            self.add_encode(encode=encode)

    def get_encode(self, encode_name: str) -> Optional[Encode]:
        """
        Get encode by name
        :param encode_name: name of encode
        :return: encode object (if exists) or None
        """
        return self.__encode_name_to_encode.get(encode_name)

    def get_encodes(self) -> List[Encode]:
        return list(self.__encode_name_to_encode.values())

    def __hash__(self):
        return hash(self.user_id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id

    def update(self, other):
        """
        Update info of user with info of another user
        """
        if not isinstance(other, User):
            return
        if self.user_id != other.user_id:
            return
        self.add_positive_posts(
            posts=other.positive_posts
        )
        self.add_negative_posts(
            posts=other.negative_posts
        )
        self.add_encodes(encodes=other.get_encodes())
