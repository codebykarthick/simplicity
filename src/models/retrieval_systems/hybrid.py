import threading
from typing import List, cast

from chromadb.base_types import Metadata

from dto.response import Abstract
from models.retrieval_systems.base import BaseRetrievalSystem
from utils.api_client import fetch_metadata
from utils.logger import setup_logger

logger = setup_logger()


class HybridRetrievalSystem(BaseRetrievalSystem):
    """The actual retrieval system that automatically switches between only remote, local or hybrid
    method for fetching relevant information.
    """

    def __init__(self, is_local, is_remote) -> None:
        """The constructor to initialise the retrieval system.

        Args:
            is_local (bool): To retrieve documents from local or not.
            is_remote (bool): To retrieve documents from remote api or not.
        """
        super().__init__()
        self.is_local = is_local
        self.is_remote = is_remote

    def fetch(self, query: str, limit: int) -> List[Abstract]:
        """Fetch the documents from local, remote or both based on the query and limit of results.

        Args:
            query (str): The query posted by the user from the UI.
            limit (int): The maximum number of records to fetch.

        Returns:
            List[Abstract]: The list of abstracts to generate the summary for.
        """
        local_abstracts = []

        if self.is_local:
            local_abstracts = self.fetch_local(query=query, limit=limit)
            logger.info(
                f"Fetched {len(local_abstracts)} from local store for the query.")

        missing_abstracts = limit - len(local_abstracts)

        if self.is_remote and missing_abstracts > 0:
            logger.info(
                f"Fetching {missing_abstracts} from remote api for the query.")
            remote_abstracts = self.fetch_remote(
                query=query, limit=missing_abstracts)

        return (local_abstracts + remote_abstracts)

    def fetch_local(self, query: str, limit: int) -> List[Abstract]:
        """The method to fetch the documents from local vector database.

        Args:
            query (str): The query posted by the user from the UI.
            limit (int): The maximum number of records to fetch.

        Returns:
            List[Abstract]: The list of abstracts to generate the summary for, from local storage.
        """
        results = self.collection.query(query_texts=[query], n_results=limit)

        # Safely extract lists or default to empty
        raw_docs = results.get("documents") or []
        raw_metas = results.get("metadatas") or []
        raw_ids = results.get("ids") or []

        # Each raw_* is a list of lists; take first list if present, else empty
        docs = raw_docs[0] if raw_docs and isinstance(
            raw_docs[0], list) else []
        metadatas = raw_metas[0] if raw_metas and isinstance(
            raw_metas[0], list) else []
        ids = raw_ids[0] if raw_ids and isinstance(raw_ids[0], list) else []

        abstracts = []

        for doc, meta, id_ in zip(docs, metadatas, ids):
            abstract = Abstract(
                id=cast(str, meta.get("my_id", "")),
                arxiv_id=id_,
                title=cast(str, meta.get("title", "")),
                authors=cast(str, meta.get("authors", "")),
                year=cast(str, meta.get("year", "")),
                categories=cast(str, meta.get("categories", "")),
                abstract=doc,
                pdf_url=cast(str, meta.get("pdf_url", ""))
            )
            abstracts.append(abstract)

        return abstracts

    def fetch_remote(self, query: str, limit: int) -> List[Abstract]:
        """The method to fetch the documents from the ArXiv API based on query and number of results.
        Optionally updates local store.

        Args:
            query (str): The query posted by the user from the UI.
            limit (int): The maximum number of records to fetch.

        Returns:
            List[Abstract]: The list of abstracts to generate the summary for.
        """
        abstracts = fetch_metadata(query=query, max_results=limit)

        if self.should_save:
            # Create a separate thread to persist vectors
            threading.Thread(
                target=self.process_and_save,
                args=(abstracts,),
                daemon=True
            ).start()

        return abstracts

    def process_and_save(self, abstracts: List[Abstract]) -> None:
        """Process to update the metadata and documents in the vector store.

        Args:
            abstracts (List[Abstract]): The remote abstracts to update the store.
        """
        # Update the chromadb store async
        documents = [a.abstract for a in abstracts]
        ids = [a.arxiv_id for a in abstracts]
        metadatas = [
            cast(Metadata, {
                "my_id": a.id,
                "title": a.title,
                "authors": a.authors,
                "year": a.year,
                "categories": a.categories,
                "pdf_url": a.pdf_url
            })
            for a in abstracts
        ]

        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
