import os
from typing import List

from dto.response import Abstract
from models.lm import LanguageModel
from utils.config import CONFIG


class Retriever:
    """The retriever that is responsible to handle both the vector store and the ArXiv API fallback
    to generate the final List[Abstract] list for the generator to generate the cited summary.
    """

    def __init__(self) -> None:
        ...

    def fetch(self, query: str, limit: int) -> List[Abstract]:
        """Method to fetch from both the cached vector storage and arxiv api according to the query
        and limit of results.

        Args:
            query (str): The query from the UI by the user
            limit (int): The maximum number of results

        Returns:
            List[Abstract]: The list of relevant abstracts returned.
        """
        abstracts = [
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

        return abstracts


class Generator:
    """Responsible for generating the cited summary from the sources retrieved by the Retriever, using a LM.
    """

    def __init__(self) -> None:
        prompt_path = os.path.join(
            "prompt_templates", CONFIG["generator"]["template"])
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
