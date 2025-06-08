from typing import List

from pydantic import BaseModel


class Abstract(BaseModel):
    id: str
    title: str
    authors: str
    year: str
    categories: str
    abstract: str
    pdf_url: str


class QueryResponse(BaseModel):
    summary: str
    abstracts: List[Abstract]
