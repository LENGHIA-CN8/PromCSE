"""
This package contains classes for writing general scores
"""

from .base_general_score_writer import (
    BaseGeneralScoreWriter, BaseGeneralScoreWriterConfig
)
from .base_aerospike_general_score_writer_version_1 import (
    BaseAerospikeGeneralScoreWriterVersion1,
    BaseAerospikeGeneralScoreWriterVersion1Config
)
from .general_score_writer_builder import (
    GeneralScoreWriterBuilder
)
from .aerospike_general_score_writer_version_1 import (
    AerospikeGeneralScoreWriterVersion1,
    AerospikeGeneralScoreWriterVersion1Config
)
