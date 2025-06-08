from dto.response import Abstract, QueryResponse
from utils.logger import logger


class Engine:
    """The main "system" responsible for both fetching from ArXiv API and Vector store, as well
    as using a LM to generate the response back to the user.
    """

    def __init__(self) -> None:
        """The constructor method that initialises the API client, Vector store and the LM
        instance to be used for the actual flow.
        """
        ...

    def generate_response(self, query: str, limit: int) -> QueryResponse:
        """The full RAG flow of retrieving the content from both the vector stores and ArXiv API
        and generating a summary using the configured LM.

        TODO: Replace mock response with actual structured response.

        Args:
            query (str): The query posted by the user from the UI.
            max_results (int): The maximum number of results across vector store and API combined to
            generate the results from.

        Returns:
            QueryResponse: The response to be sent back to the user.
        """
        # Check the vector store for relevant documents

        # Fetch the missing number of documents from ArXiv API

        # Combine together for the actual generation using the LM.

        # Process the obtained response
        response = QueryResponse(
            summary="Universal Transformers introduce recurrence over depth to improve generalization in sequence tasks [UT]. We can use different algorithms that involve transforms to solve a reinforcement problem. [TR].",
            abstracts=[
                Abstract(
                    id="UT",
                    title="Universal Transformers",
                    authors=[
                        "Mostafa Dehghani", "Stephan Gouws", "Oriol Vinyals",
                        "Jakob Uszkoreit", "Łukasz Kaiser"
                    ],
                    year="2019",
                    categories=["cs.CL"],
                    abstract=(
                        "Universal Transformers generalize the standard Transformer by introducing recurrence "
                        "over depth, allowing dynamic halting per token and achieving better generalization on "
                        "language and algorithmic tasks. They combine the parallelism of Transformers with the "
                        "inductive bias of RNNs and achieve state-of-the-art results on tasks like bAbI and LAMBADA."
                    ),
                    pdf_url="https://arxiv.org/pdf/1807.03819"
                ),
                Abstract(
                    id="TR",
                    title="Transformers in Reinforcement Learning: A Survey",
                    authors=[
                        "Pranav Agarwal", "Aamer Abdul Rahman", "Pierre-Luc St-Charles", "Simon J.D. Prince", "Samira Ebrahimi Kahou"
                    ],
                    year="2023",
                    categories=["cs.LG"],
                    abstract=(
                        "Transformers have significantly impacted domains like natural language processing, computer vision, and"
                        "robotics, where they improve performance compared to other neural networks. This survey explores how"
                        "transformers are used in reinforcement learning (RL), where they are seen as a promising solution for address-"
                        "ing challenges such as unstable training, credit assignment, lack of interpretability, and partial observability."
                    ),
                    pdf_url="https://arxiv.org/pdf/2307.05979"
                ),
            ][:limit]
        )

        logger.info(
            f"Query: {query}, generated content from {len(response.abstracts)} sources.")

        return response
