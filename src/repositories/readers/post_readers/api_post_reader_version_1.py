from typing import List, Dict, Optional
from logger import SingletonLogger
from objects import Post
from .base_post_reader import (
    BasePostReader, BasePostReaderConfig
)
from datetime import date, timedelta
import requests
from tqdm import tqdm
import json


class ApiPostReaderVersion1(BasePostReader):
    """
    Read post's num clicks, num views from Api
    """
    def __init__(
            self, source_news: str, url: str,
            num_days: int, batch_size: int, verbose: bool
    ):
        """
        Init method
        :param source_news: source news to get data
        :param url: url to get info
        :param num_days: number of days to get data
        :param batch_size: batch size of reading
        :param verbose: display progress bar while reading
        """
        super(ApiPostReaderVersion1, self).__init__()
        self.source_news = source_news
        self.url = url
        self.num_days = num_days
        self.batch_size = batch_size
        self.verbose = verbose

    @property
    def source_news(self) -> str:
        return self._source_news

    @source_news.setter
    def source_news(self, source_news: str):
        assert isinstance(source_news, str)
        self._source_news: str = source_news

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        assert isinstance(url, str)
        self._url: str = url

    @property
    def num_days(self) -> int:
        return self._num_days

    @num_days.setter
    def num_days(self, num_days: int):
        assert isinstance(num_days, int)
        self._num_days: int = num_days

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int):
        assert isinstance(batch_size, int)
        self._batch_size: int = batch_size
        
    @property
    def verbose(self) -> bool:
        return self._verbose
    
    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose

    def read_post(self, post: Post) -> bool:
        """
        Read info of a post
        :param post: post to read info
        :return: True if success, else False
        """
        return self.read_posts(
            posts=[post]
        )

    def _get_request_params(self, posts: List[Post]) -> Dict:
        """
        Get params of the requests
        :param posts: list post to get data
        :return: params
        """
        finish_date: date = date.today()
        start_date: date = finish_date - timedelta(days=self.num_days)
        return {
            "domain": self.source_news,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "finish_date": finish_date.strftime("%Y-%m-%d"),
            "items": [
                str(post.post_id) for post in posts
            ]
        }

    def _instance_to_post(self, instance: object) -> Optional[Post]:
        """
        Convert instance data to post
        :param instance: instance to convert
        :return: post object or None if failed
        """
        if not isinstance(instance, dict):
            return None
        post_id = instance.get("newsId")
        if (
                not isinstance(post_id, str) or
                not post_id.isdigit()
        ):
            return None
        post_id: int = int(post_id)
        num_clicks = instance.get("click")
        if not isinstance(num_clicks, int):
            num_clicks = 0
        num_views = instance.get("view")
        if not isinstance(num_views, int):
            num_views = 0
        return Post(
            post_id=post_id, num_clicks=num_clicks,
            num_views=num_views
        )

    def _read_posts(self, posts: List[Post]) -> bool:
        """
        Read info of a collection of posts
        :param posts: posts to read info
        :return: True if success, else False
        """
        try:
            response = requests.get(
                url=self.url,
                data=json.dumps(
                    self._get_request_params(posts=posts)
                )
            ).json()
            if (
                not isinstance(response, dict) or
                "results" not in response or
                not isinstance(response["results"], list)
            ):
                return False
            post_to_query_post: Dict[Post, Post] = {}
            for instance in response["results"]:
                query_post: Optional[Post] = self._instance_to_post(
                    instance=instance
                )
                if query_post:
                    post_to_query_post[query_post] = query_post
            for post in posts:
                post.update(
                    other=post_to_query_post.get(post)
                )
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading posts clicks views from API"
            )
            return False

    def read_posts(self, posts: List[Post]) -> bool:
        """
        Read info of a collection of posts
        :param posts: posts to read info
        :return: True if success, else False
        """
        if self.verbose:
            status: bool = True
            progress_bar = tqdm(
                iterable=range(0, len(posts), self.batch_size),
                desc="Reading posts num clicks, views..."
            )
            for start_idx in progress_bar:
                end_idx: int = min(start_idx + self.batch_size, len(posts))
                status = self._read_posts(
                    posts=posts[start_idx:end_idx]
                ) and status
            progress_bar.close()
            return status
        else:
            status: bool = True
            for start_idx in range(0, len(posts), self.batch_size):
                end_idx: int = min(start_idx+self.batch_size, len(posts))
                status = self._read_posts(
                    posts=posts[start_idx:end_idx]
                ) and status
            return status


class ApiPostReaderVersion1Config(BasePostReaderConfig):
    """
    Config for read post's num clicks, num views from Api
    """
    def __init__(
            self, source_news: str, url: str,
            num_days: int, batch_size: int, verbose: bool
    ):
        """
        Init method
        :param source_news: source news to get data
        :param url: url to get info
        :param num_days: number of days to get data
        :param batch_size: batch size of reading
        :param verbose: display progress bar while reading
        """
        super(ApiPostReaderVersion1Config, self).__init__()
        self.source_news = source_news
        self.url = url
        self.num_days = num_days
        self.batch_size = batch_size
        self.verbose = verbose

    @property
    def source_news(self) -> str:
        return self._source_news

    @source_news.setter
    def source_news(self, source_news: str):
        assert isinstance(source_news, str)
        self._source_news: str = source_news

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        assert isinstance(url, str)
        self._url: str = url

    @property
    def num_days(self) -> int:
        return self._num_days

    @num_days.setter
    def num_days(self, num_days: int):
        assert isinstance(num_days, int)
        self._num_days: int = num_days

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int):
        assert isinstance(batch_size, int)
        self._batch_size: int = batch_size

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose
