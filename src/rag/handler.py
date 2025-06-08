import os
from typing import List

from dto.response import Abstract
from models.lm import LanguageModel
from models.retrieval_systems.hybrid import HybridRetrievalSystem
from models.retrieval_systems.mock import MockRetrievalSystem
from utils.config import load_config
from utils.constants import Constants
from utils.logger import setup_logger

logger = setup_logger()
config = load_config()


class Retriever:
    """The retriever that is responsible to handle both the vector store and the ArXiv API fallback
    to generate the final List[Abstract] list for the generator to generate the cited summary.
    """

    def __init__(self) -> None:
        ret_config = config[Constants.RETRIVER]
        mode = ret_config[Constants.MODE].lower()
        logger.info(f"Creating a '{mode}' retrieval system instance.")

        if mode == "mock":
            self.system = MockRetrievalSystem()
        elif mode == "local":
            self.system = HybridRetrievalSystem(is_local=True, is_remote=False)
        elif mode == "remote":
            self.system = HybridRetrievalSystem(is_local=False, is_remote=True)
        elif mode == "hybrid":
            self.system = HybridRetrievalSystem(is_local=True, is_remote=True)
        else:
            logger.warning(
                f"'{mode}' is not recognized; defaulting to mock retrieval.")
            self.system = MockRetrievalSystem()

    def fetch(self, query: str, limit: int) -> List[Abstract]:
        """Method to fetch from both the cached vector storage and arxiv api according to the query
        and limit of results.

        Args:
            query (str): The query from the UI by the user
            limit (int): The maximum number of results

        Returns:
            List[Abstract]: The list of relevant abstracts returned.
        """
        return self.system.fetch(query=query, limit=limit)


class Generator:
    """Responsible for generating the cited summary from the sources retrieved by the Retriever, using a LM.
    """

    def __init__(self) -> None:
        logger.info(
            f"Loading prompt: {config['generator']['template']} for generation.")
        prompt_path = os.path.join(
            "prompt_templates", config["generator"]["template"])
        with open(prompt_path, "r") as f:
            self.base_prompt = f.read()
        self.lang_model = LanguageModel()

    def summarize(self, query: str, abstracts: List[Abstract]) -> str:
        """Use the LM to generate the cited summary from the list of abstracts retrieved by the retriever.

        Args:
            query (str): The original query posted by the user for LM guidance.
            abstracts (List[Abstract]): The list of abstracts relevant to the query provided by the user.

        Returns:
            str: The cited summary returned by the LM.
        """
        sources_str = "\n\n".join(
            f"[{abstract.id}] - \"{abstract.abstract}\"" for abstract in abstracts
        )
        prompt = self.base_prompt.format(
            query=query, sources=sources_str)

        # Use the language model (mock or real) to generate summary
        return self.lang_model.generate(prompt)
