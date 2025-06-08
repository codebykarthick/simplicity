from enum import Enum


class Constants(str, Enum):
    ARXIV = "arxiv"
    URL = "url"
    MAX_RESULTS = "max_results"
    GENERATOR = "generator"
    RETRIVER = "retriever"
    MODE = "mode"
    LM = "lm"
    TEMPERATURE = "temperature"
    MAX_TOKENS = "max_tokens"
