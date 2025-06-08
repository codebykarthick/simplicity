from typing import List

from dto.response import Abstract
from models.retrieval_systems.base import BaseRetrievalSystem


class LocalRetrievalSystem(BaseRetrievalSystem):
    def __init__(self) -> None:
        super().__init__()

    def fetch(self, query: str, limit: int) -> List[Abstract]:
        raise NotImplementedError("fetch method not implemented!")
