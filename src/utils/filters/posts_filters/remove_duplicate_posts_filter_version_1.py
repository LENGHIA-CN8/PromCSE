from typing import List, Set
from objects import Post
from .base_posts_filter import (
    BasePostsFilter, BasePostsFilterConfig
)
from logger import SingletonLogger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import numpy as np


class RemoveDuplicatePostsFilterVersion1(BasePostsFilter):
    """
    Remove duplicate posts by using cosine similarity on Tfidf vector compute from title and sapo
    """
    def __init__(
            self, threshold: float
    ):
        """
        Init method
        :param threshold: similarity threshold for posts to be removed
        """
        super(RemoveDuplicatePostsFilterVersion1, self).__init__()
        self.threshold = threshold

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: float):
        assert isinstance(threshold, float)
        self._threshold: float = threshold

    def _get_text(self, post: Post) -> str:
        """
        Get text representation for post
        :param post: post to get text
        :return: string
        """
        return (post.title or "") + " . " + (post.sapo or "")

    def filter_posts(
            self, posts: List[Post]
    ) -> List[Post]:
        """
        Remove invalid posts
        :param posts: list of posts
        :return: list valid posts
        """
        try:
            if len(posts) <= 1:
                return posts
            # get cosine score
            documents: List[str] = [
                self._get_text(post=post) for post in posts
            ]
            tfidf_matrix: csr_matrix = TfidfVectorizer().fit_transform(
                raw_documents=documents
            )
            cosine_matrix: np.ndarray = cosine_similarity(
                tfidf_matrix
            )
            # filter posts
            kept_posts: List[Post] = []
            removed_posts: Set[Post] = set()
            for i in range(0, len(posts)):
                post_i: Post = posts[i]
                if post_i in removed_posts:
                    continue
                kept_posts.append(post_i)
                for j in range(i+1, len(posts)):
                    if cosine_matrix[i, j] >= self.threshold:
                        removed_posts.add(posts[j])
            return kept_posts
        except:
            SingletonLogger.get_instance().exception(
                "Exception while removing duplicate posts"
            )
            return posts


class RemoveDuplicatePostsFilterVersion1Config(BasePostsFilterConfig):
    """
    Config for remove duplicate posts by using cosine similarity on Tfidf vector compute from title and sapo
    """
    def __init__(
            self, threshold: float
    ):
        """
        Init method
        :param threshold: similarity threshold for posts to be removed
        """
        super(RemoveDuplicatePostsFilterVersion1Config, self).__init__()
        self.threshold = threshold

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: float):
        assert isinstance(threshold, float)
        self._threshold: float = threshold
