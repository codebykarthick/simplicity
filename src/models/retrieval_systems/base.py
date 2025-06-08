from abc import ABC, abstractmethod
from typing import List

from dto.response import Abstract


class BaseRetrievalSystem(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def fetch(self, query: str, limit: int) -> List[Abstract]:
        raise NotImplementedError("fetch method not implemented!")
