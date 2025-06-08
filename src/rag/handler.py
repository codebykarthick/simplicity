from typing import List

from dto.response import Abstract


class Retriever:
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
    def __init__(self) -> None:
        ...

    def summarize(self, abstracts: List[Abstract]) -> str:
        """Use the LM to generate the cited summary from the list of abstracts retrieved by the retriever.

        Args:
            abstracts (List[Abstract]): The list of abstracts relevant to the query provided by the user.

        Returns:
            str: The cited summary returned by the LM.
        """

        summary = "Universal Transformers introduce recurrence over depth to improve generalization " + \
            "in sequence tasks [UT]. We can use different algorithms that involve transforms to solve" + \
            "a reinforcement problem. [TR]."

        return summary
