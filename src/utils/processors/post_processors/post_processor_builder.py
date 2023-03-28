from .base_post_processor import (
    BasePostProcessor, BasePostProcessorConfig
)
from .content_post_processor_version_1 import (
    ContentPostProcessorVersion1,
    ContentPostProcessorVersion1Config
)
from utils.processors.text_processors import (
    TextProcessorBuilder
)


class PostProcessorBuilder:
    """
    Class for building post processor
    """
    @classmethod
    def build_post_processor(
            cls, config: BasePostProcessorConfig
    ) -> BasePostProcessor:
        if isinstance(config, ContentPostProcessorVersion1Config):
            return ContentPostProcessorVersion1(
                text_processor=TextProcessorBuilder.build_text_processor(
                    config=config.text_processor_config
                ) if config.text_processor_config is not None else None,
                title_processor=TextProcessorBuilder.build_text_processor(
                    config=config.title_processor_config
                ) if config.title_processor_config is not None else None,
                sapo_processor=TextProcessorBuilder.build_text_processor(
                    config=config.sapo_processor_config
                ) if config.sapo_processor_config is not None else None,
                body_processor=TextProcessorBuilder.build_text_processor(
                    config=config.body_processor_config
                ) if config.body_processor_config is not None else None,
                verbose=config.verbose
            )
        else:
            raise ValueError(
                f"Invalid post processor class: {config}"
            )
