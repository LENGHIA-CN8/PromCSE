from .base_trending_context_reader import (
    BaseTrendingContextReader,
    BaseTrendingContextReaderConfig
)
from .api_trending_context_reader_version_1 import (
    ApiTrendingContextReaderVersion1,
    ApiTrendingContextReaderVersion1Config
)


class TrendingContextReaderBuilder:
    """
    Class for building trending context reader
    """
    @classmethod
    def build_trending_context_reader(
            cls, config: BaseTrendingContextReaderConfig
    ) -> BaseTrendingContextReader:
        if isinstance(config, ApiTrendingContextReaderVersion1Config):
            return ApiTrendingContextReaderVersion1(
                url=config.url
            )
        else:
            raise ValueError(
                f"Invalid trending context reader: {config}"
            )
