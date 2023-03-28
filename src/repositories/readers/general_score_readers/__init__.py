"""
This packages contains classes for reading general score
"""


from .base_general_score_reader import (
    BaseGeneralScoreReader, BaseGeneralScoreReaderConfig
)
from .base_aerospike_general_score_reader_version_1 import (
    BaseAerospikeGeneralScoreReaderVersion1Config,
    BaseAerospikeGeneralScoreReaderVersion1
)
from .general_score_reader_builder import (
    GeneralScoreReaderBuilder
)
from .aerospike_general_score_reader_version_1 import (
    AerospikeGeneralScoreReaderVersion1,
    AerospikeGeneralScoreReaderVersion1Config
)
