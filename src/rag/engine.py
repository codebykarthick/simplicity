from dto.response import QueryResponse
from rag.handler import Generator, Retriever
from utils.logger import logger


class Engine:
    """The main "system" responsible for both fetching from ArXiv API and Vector store, as well
    as using a LM to generate the response back to the user.
    """

    def __init__(self) -> None:
        """The constructor method that initialises the API client, Vector store and the LM
        instance to be used for the actual flow.
        """
        self.retriever = Retriever()
        self.generator = Generator()

    def generate_response(self, query: str, limit: int) -> QueryResponse:
        """The full RAG flow of retrieving the content from both the vector stores and ArXiv API
        and generating a summary using the configured LM.

        Args:
            query (str): The query posted by the user from the UI.
            max_results (int): The maximum number of results across vector store and API combined to
            generate the results from.

        Returns:
            QueryResponse: The response to be sent back to the user.
        """
        # Check the vector store for relevant documents & fetch the missing number of documents from ArXiv
        abstracts = self.retriever.fetch(query=query, limit=limit)

        # Combine together for the actual generation using the LM.
        summary = self.generator.summarize(query=query, abstracts=abstracts)

        # Process the obtained response
        response = QueryResponse(
            summary=summary,
            abstracts=abstracts
        )

        logger.info(
            f"Query: {query}, generated content from {len(abstracts)} sources.")

        return response
