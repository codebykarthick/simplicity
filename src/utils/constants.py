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
    SAVE = "save"
    SAVE_FOLDER = "save_folder"
    COL_DOC = "collection_docs"
    HF_KEY = "hf-key"
