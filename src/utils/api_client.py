import xml.etree.ElementTree as ET
from time import time
from typing import List, cast

import requests

from dto.response import Abstract
from utils.config import load_config
from utils.constants import Constants
from utils.logger import setup_logger
from utils.timer import timeit

logger = setup_logger
config = load_config()

# Unpack the constants needed for this module.
ARXIV_API_URL = config[Constants.ARXIV][Constants.URL]
MAX_ARXIV_RESULTS = config[Constants.ARXIV][Constants.URL]


@timeit
def fetch_metadata(query: str, max_results: int = MAX_ARXIV_RESULTS) -> List[Abstract]:
    """Query the arXiv API with `query` and return a list of metadata dicts.
    Each dict contains: id, title, abstract, authors, published, categories.

    Args:
        query (str): The query to fetch the results for.
        max_results (int, optional): The maximum number of results needed for the query. Defaults to MAX_ARXIV_RESULTS.

    Returns:
        List[Abstract]: The list of relevant papers' metadata returned by ArXiv
    """
    # Build the request URL and parameters
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results
    }

    try:
        response = requests.get(ARXIV_API_URL, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Error fetching arXiv data for query='{query}': {e}")
        return []

    # Parse the XML response
    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        logger.error(f"Failed to parse arXiv XML: {e}")
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []
    for entry in root.findall("atom:entry", ns):
        try:
            title_node = entry.find("atom:title", ns)
            summary_node = entry.find("atom:summary", ns)
            published_node = entry.find("atom:published", ns)
            pdf_url = None

            for link in entry.findall("atom:link", ns):
                if link.attrib.get("type") == "application/pdf":
                    pdf_url = link.attrib.get("href")
                    break

            if title_node and summary_node and published_node:
                # Parse the title node
                title = cast(str, title_node.text).strip().replace("\n", " ")

                # Parse a better ID than the one returned by ArXiv
                words = title.split()
                upper_words = [
                    word for word in words if word and word[0].isupper()]
                my_id = ''.join(word[0] for word in upper_words[:2]) if len(
                        upper_words) >= 2 else title[:2].upper()

                # Get the abstract and other data
                abstract = cast(
                    str, summary_node.text).strip().replace("\n", " ")
                published = cast(str, published_node.text)

                # Authors
                authors = [
                    name_tag.text
                    for author in entry.findall("atom:author", ns)
                    if (name_tag := author.find("atom:name", ns)) is not None and name_tag.text
                ]

                # Categories
                categories = [
                    cat.attrib.get("term", "")
                    for cat in entry.findall("atom:category", ns)
                ]

                papers.append(Abstract(
                    id=my_id,
                    title=title,
                    abstract=abstract,
                    authors=", ".join(authors),
                    year=published[:4],
                    categories=", ".join(categories),
                    pdf_url=pdf_url or ""
                ))
            else:
                logger.warning(
                    "Error in parsing, some of the nodes are empty!")
        except Exception as parse_err:
            logger.warning(
                f"Skipped an entry due to parsing error: {parse_err}")
            continue

    logger.info(
        f"Fetched {len(papers)} papers for query='{query}'.")
    return papers
