from abc import ABC, abstractmethod
from typing import List

import chromadb

from dto.response import Abstract
from utils.config import load_config
from utils.constants import Constants


class BaseRetrievalSystem(ABC):
    """The base interface which the other retrieval systems will implement their functionality
    through.
    """

    def __init__(self) -> None:
        super().__init__()
        config = load_config()
        ret_config = config[Constants.RETRIVER]

        self.save_folder = ret_config[Constants.SAVE_FOLDER]
        self.collection_docs = ret_config[Constants.COL_DOC]
        self.should_save = ret_config[Constants.SAVE]
        self.threshold = ret_config[Constants.THRESHOLD]

        self.client = chromadb.PersistentClient(
            path=self.save_folder
        )
        self.collection = self.client.get_or_create_collection(
            self.collection_docs
        )

    @abstractmethod
    def fetch(self, query: str, limit: int) -> List[Abstract]:
        raise NotImplementedError("fetch method not implemented!")
