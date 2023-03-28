from objects import Post
from .base_element_wise_post_processor import (
    BaseElementWisePostProcessor,
    BaseElementWisePostProcessorConfig
)
from utils.processors.text_processors import (
    BaseTextProcessor, BaseTextProcessorConfig
)
from typing import Optional


class ContentPostProcessorVersion1(BaseElementWisePostProcessor):
    """
    Process post title, sapo, body of post
    """
    def __init__(
            self, text_processor: Optional[BaseTextProcessor],
            title_processor: Optional[BaseTextProcessor],
            sapo_processor: Optional[BaseTextProcessor],
            body_processor: Optional[BaseTextProcessor],
            verbose: bool
    ):
        """
        Init method
        :param text_processor: processor apply to both title, sapo, body
        :param title_processor: processor apply to title
        :param sapo_processor: processor apply to sapo
        :param body_processor: processor apply to body
        :param verbose: display progress bar
        """
        super(ContentPostProcessorVersion1, self).__init__(
            verbose=verbose
        )
        self.text_processor = text_processor
        self.title_processor = title_processor
        self.sapo_processor = sapo_processor
        self.body_processor = body_processor

    @property
    def text_processor(self) -> Optional[BaseTextProcessor]:
        return self._text_processor

    @text_processor.setter
    def text_processor(self, text_processor: Optional[BaseTextProcessor]):
        if text_processor is not None:
            assert isinstance(text_processor, BaseTextProcessor)
        self._text_processor: Optional[BaseTextProcessor] = text_processor

    @property
    def title_processor(self) -> Optional[BaseTextProcessor]:
        return self._title_processor

    @title_processor.setter
    def title_processor(self, title_processor: Optional[BaseTextProcessor]):
        if title_processor is not None:
            assert isinstance(title_processor, BaseTextProcessor)
        self._title_processor: Optional[BaseTextProcessor] = title_processor

    @property
    def sapo_processor(self) -> Optional[BaseTextProcessor]:
        return self._sapo_processor

    @sapo_processor.setter
    def sapo_processor(self, sapo_processor: Optional[BaseTextProcessor]):
        if sapo_processor is not None:
            assert isinstance(sapo_processor, BaseTextProcessor)
        self._sapo_processor: Optional[BaseTextProcessor] = sapo_processor

    @property
    def body_processor(self) -> Optional[BaseTextProcessor]:
        return self._body_processor

    @body_processor.setter
    def body_processor(self, body_processor: Optional[BaseTextProcessor]):
        if body_processor is not None:
            assert isinstance(body_processor, BaseTextProcessor)
        self._body_processor: Optional[BaseTextProcessor] = body_processor

    def process_post(self, post: Post):
        """
        Process post inplace
        :param post: post to process
        :return: None
        """
        if self.text_processor:
            if post.title:
                post.title = self.text_processor.process_text(
                    text=post.title
                )
            if post.sapo:
                post.sapo = self.text_processor.process_text(
                    text=post.sapo
                )
            if post.body:
                post.body = self.text_processor.process_text(
                    text=post.body
                )
        if self.title_processor and post.title:
            post.title = self.title_processor.process_text(
                text=post.title
            )
        if self.sapo_processor and post.sapo:
            post.sapo = self.sapo_processor.process_text(
                text=post.sapo
            )
        if self.body_processor and post.body:
            post.body = self.body_processor.process_text(
                text=post.body
            )


class ContentPostProcessorVersion1Config(BaseElementWisePostProcessorConfig):
    """
    Config for process post title, sapo, body of post
    """
    def __init__(
            self, text_processor_config: Optional[BaseTextProcessorConfig],
            title_processor_config: Optional[BaseTextProcessorConfig],
            sapo_processor_config: Optional[BaseTextProcessorConfig],
            body_processor_config: Optional[BaseTextProcessorConfig],
            verbose: bool
    ):
        """
        Init method
        :param text_processor_config: processor apply to both title, sapo, body
        :param title_processor_config: processor apply to title
        :param sapo_processor_config: processor apply to sapo
        :param body_processor_config: processor apply to body
        :param verbose: display progress bar
        """
        super(ContentPostProcessorVersion1Config, self).__init__(
            verbose=verbose
        )
        self.text_processor_config = text_processor_config
        self.title_processor_config = title_processor_config
        self.sapo_processor_config = sapo_processor_config
        self.body_processor_config = body_processor_config

    @property
    def text_processor_config(self) -> Optional[BaseTextProcessorConfig]:
        return self._text_processor_config

    @text_processor_config.setter
    def text_processor_config(self, text_processor_config: Optional[BaseTextProcessorConfig]):
        if text_processor_config is not None:
            assert isinstance(text_processor_config, BaseTextProcessorConfig)
        self._text_processor_config: Optional[BaseTextProcessorConfig] = text_processor_config

    @property
    def title_processor_config(self) -> Optional[BaseTextProcessorConfig]:
        return self._title_processor_config

    @title_processor_config.setter
    def title_processor_config(self, title_processor_config: Optional[BaseTextProcessorConfig]):
        if title_processor_config is not None:
            assert isinstance(title_processor_config, BaseTextProcessorConfig)
        self._title_processor_config: Optional[BaseTextProcessorConfig] = title_processor_config

    @property
    def sapo_processor_config(self) -> Optional[BaseTextProcessorConfig]:
        return self._sapo_processor_config

    @sapo_processor_config.setter
    def sapo_processor_config(self, sapo_processor_config: Optional[BaseTextProcessorConfig]):
        if sapo_processor_config is not None:
            assert isinstance(sapo_processor_config, BaseTextProcessorConfig)
        self._sapo_processor_config: Optional[BaseTextProcessorConfig] = sapo_processor_config

    @property
    def body_processor_config(self) -> Optional[BaseTextProcessorConfig]:
        return self._body_processor_config

    @body_processor_config.setter
    def body_processor_config(self, body_processor_config: Optional[BaseTextProcessorConfig]):
        if body_processor_config is not None:
            assert isinstance(body_processor_config, BaseTextProcessorConfig)
        self._body_processor_config: Optional[BaseTextProcessorConfig] = body_processor_config
