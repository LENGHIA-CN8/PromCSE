from typing import Optional, Iterable, Dict, List
from datetime import datetime
from .encode import Encode


class Post:
    """
    Class represent a post object
    """
    def __init__(
            self, post_id: int,
            title: Optional[str] = None, sapo: Optional[str] = None,
            body: Optional[str] = None,
            tags: Optional[str] = None, ners: Optional[str] = None,
            category: Optional[int] = None,
            publish_date: Optional[datetime] = None,
            num_clicks: Optional[int] = None, num_views: Optional[int] = None,
            encode: Optional[Encode] = None, encodes: Optional[Iterable[Encode]] = None
    ):
        """
        Init method
        :param post_id: id of post
        :param title: title of post
        :param sapo: sapo of post
        :param body: body of post
        :param tags: tags of post
        :param ners: ners of post
        :param category: category of post
        :param publish_date: publish date of post
        :param num_clicks: number clicks of post
        :param num_views: number views of post
        :param encode: encode of post
        :param encodes: list encodes of post
        """
        self.__encode_name_to_encode: Dict[str, Encode] = {}
        self.post_id = post_id
        self.title = title
        self.sapo = sapo
        self.body = body
        self.tags = tags
        self.ners = ners
        self.category = category
        self.publish_date = publish_date
        self.num_clicks = num_clicks
        self.num_views = num_views
        if encode is not None:
            self.add_encode(encode=encode)
        if encodes is not None:
            self.add_encodes(encodes=encodes)

    @property
    def post_id(self) -> int:
        return self._post_id

    @post_id.setter
    def post_id(self, post_id: int):
        assert isinstance(post_id, int)
        self._post_id: int = post_id
    
    @property
    def title(self) -> Optional[str]:
        return self._title
    
    @title.setter
    def title(self, title: Optional[str]):
        if title is not None:
            assert isinstance(title, str)
        self._title: Optional[str] = title
        
    @property
    def sapo(self) -> Optional[str]:
        return self._sapo
    
    @sapo.setter
    def sapo(self, sapo: Optional[str]):
        if sapo is not None:
            assert isinstance(sapo, str)
        self._sapo: Optional[str] = sapo
        
    @property
    def body(self) -> Optional[str]:
        return self._body
    
    @body.setter
    def body(self, body: Optional[str]):
        if body is not None:
            assert isinstance(body, str)
        self._body: Optional[str] = body
        
    @property
    def tags(self) -> Optional[str]:
        return self._tags
    
    @tags.setter
    def tags(self, tags: Optional[str]):
        if tags is not None:
            assert isinstance(tags, str)
        self._tags: Optional[str] = tags

    @property
    def ners(self) -> Optional[str]:
        return self._ners

    @ners.setter
    def ners(self, ners: Optional[str]):
        if ners is not None:
            assert isinstance(ners, str)
        self._ners: Optional[str] = ners

    @property
    def category(self) -> Optional[int]:
        return self._category

    @category.setter
    def category(self, category: Optional[int]):
        if category is not None:
            assert isinstance(category, int)
        self._category: Optional[int] = category
        
    @property
    def publish_date(self) -> Optional[datetime]:
        return self._publish_date

    @publish_date.setter
    def publish_date(self, publish_date: Optional[datetime]):
        if publish_date is not None:
            assert isinstance(publish_date, datetime)
        self._publish_date: Optional[datetime] = publish_date

    @property
    def num_clicks(self) -> Optional[int]:
        return self._num_clicks

    @num_clicks.setter
    def num_clicks(self, num_clicks: Optional[int]):
        if num_clicks is not None:
            assert isinstance(num_clicks, int)
        self._num_clicks: Optional[int] = num_clicks

    @property
    def num_views(self) -> Optional[int]:
        return self._num_views

    @num_views.setter
    def num_views(self, num_views: Optional[int]):
        if num_views is not None:
            assert isinstance(num_views, int)
        self._num_views: Optional[int] = num_views

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
        return hash(self.post_id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Post):
            return False
        return self.post_id == other.post_id

    def update(self, other):
        """
        Update info on current object with info of other object
        :param other: other object to update info
        """
        if not isinstance(other, Post):
            return
        if self.post_id != other.post_id:
            return
        if other.title:
            self.title = other.title
        if other.sapo:
            self.sapo = other.sapo
        if other.body:
            self.body = other.body
        if other.tags:
            self.tags = other.tags
        if other.ners:
            self.ners = other.ners
        if other.category:
            self.category = other.category
        if other.publish_date:
            self.publish_date = other.publish_date
        if other.num_clicks:
            self.num_clicks = other.num_clicks
        if other.num_views:
            self.num_views = other.num_views
        self.add_encodes(encodes=other.get_encodes())
