from typing import Optional, List, Set
from objects import User, Post
from .base_user_posts_reader import (
    BaseUserPostsReader, BaseUserPostsReaderConfig
)


class ChainUserPostsReaderVersion1(BaseUserPostsReader):
    """
    Class for connect between reader
    """
    def __init__(
            self, readers: List[BaseUserPostsReader]
    ):
        """
        Init method
        :param readers: list of reader
        """
        super(ChainUserPostsReaderVersion1, self).__init__()
        self.readers = readers

    @property
    def readers(self) -> List[BaseUserPostsReader]:
        return self._readers

    @readers.setter
    def readers(self, readers: List[BaseUserPostsReader]):
        assert isinstance(readers, list)
        assert all(map(lambda x: isinstance(x, BaseUserPostsReader), readers))
        self._readers: List[BaseUserPostsReader] = readers

    def read_user(
            self, user: User
    ) -> Optional[List[Post]]:
        """
        Read list posts related to user
        :param user: user to read
        :return: list posts related to user, or None
        """
        result: Set[Post] = set()
        for reader in self.readers:
            posts: Optional[List[Post]] = reader.read_user(
                user=user
            )
            if posts:
                result.update(posts)
        return list(result)


class ChainUserPostsReaderVersion1Config(BaseUserPostsReaderConfig):
    """
    Class for connect between reader
    """
    def __init__(
            self, readers_config: List[BaseUserPostsReaderConfig]
    ):
        """
        Init method
        :param readers_config: list of reader
        """
        super(ChainUserPostsReaderVersion1Config, self).__init__()
        self.readers_config = readers_config

    @property
    def readers_config(self) -> List[BaseUserPostsReaderConfig]:
        return self._readers_config

    @readers_config.setter
    def readers_config(self, readers_config: List[BaseUserPostsReaderConfig]):
        assert isinstance(readers_config, list)
        assert all(map(lambda x: isinstance(x, BaseUserPostsReaderConfig), readers_config))
        self._readers_config: List[BaseUserPostsReaderConfig] = readers_config
