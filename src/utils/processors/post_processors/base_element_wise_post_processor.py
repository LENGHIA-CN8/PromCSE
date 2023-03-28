from typing import List
from objects import Post
from .base_post_processor import (
    BasePostProcessor, BasePostProcessorConfig
)
from abc import ABC
from tqdm import tqdm


class BaseElementWisePostProcessor(BasePostProcessor, ABC):
    """
    Base class for process list posts element-wise
    """
    def __init__(self, verbose: bool):
        """
        Init method
        :param verbose: display progress bar
        """
        super(BaseElementWisePostProcessor, self).__init__()
        self.verbose = verbose

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose

    def process_posts(self, posts: List[Post]):
        """
        Process collection of posts
        :param posts: collection of posts to process
        :return: None
        """
        if self.verbose:
            progress_bar = tqdm(
                iterable=posts,
                desc="Processing posts..."
            )
            for post in progress_bar:
                self.process_post(
                    post=post
                )
            progress_bar.close()
        else:
            for post in posts:
                self.process_post(
                    post=post
                )


class BaseElementWisePostProcessorConfig(BasePostProcessorConfig, ABC):
    """
    Base class for process list posts element-wise
    """
    def __init__(self, verbose: bool):
        """
        Init method
        :param verbose: display progress bar
        """
        super(BaseElementWisePostProcessorConfig, self).__init__()
        self.verbose = verbose

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose
