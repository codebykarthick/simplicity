from typing import List

from pydantic import BaseModel


class Abstract(BaseModel):
    id: str
    title: str
    authors: List[str]
    year: str
    categories: List[str]
    abstract: str
    pdf_url: str


class QueryResponse(BaseModel):
    summary: str
    abstracts: List[Abstract]
