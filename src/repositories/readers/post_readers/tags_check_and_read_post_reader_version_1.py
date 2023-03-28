from objects import Post
from .base_check_and_read_post_reader_version_1 import (
    BaseCheckAndReadPostReaderVersion1,
    BaseCheckAndReadPostReaderVersion1Config
)


class TagsCheckAndReadPostReaderVersion1(BaseCheckAndReadPostReaderVersion1):
    """
    Check if post have tags, if not => read
    """
    def _is_need_to_read(self, post: Post) -> bool:
        """
        Check if we need to read post info
        :param post: post to check
        :return: True if need to read, else False
        """
        if post.tags:
            return False
        else:
            return True


class TagsCheckAndReadPostReaderVersion1Config(BaseCheckAndReadPostReaderVersion1Config):
    """
    Config for check if post have tags, if not => read
    """
    pass
