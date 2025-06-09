# simplicity
A hybrid RAG based on Arxiv metadata API. Discussed in depth in [this multi-part blog post.](https://codebykarthick.github.io/projects/2025-06-09-simplicity-1/)

## Introduction
The aim of this RAG is to provide a simple web interface through which an user can post queries along with the maximum number of results they want to be fetched for generation. The query is first checked against the local vector store, if no results are sufficient, it then searches arxiv metadata api for relevant content. This fetched content of title, authors, abstract and id is then both cached in the vector database (ChromaDB) and also simultaneously fed into the LLM to generate a cited summary of all the abstracts. This resulting summary, along with its citations are displayed.

## Setup and Execution
Since the LLM is run locally for inference, running this project needs a lot of memory (CPU or GPU). To install the required dependencies run

```bash
pip install -r requirements.txt
```

and to start the web server run the following command in the `src/` directory.

```bash
# Dev mode automatically reloads on code change
uvicorn app:server --host 0.0.0.0 --reload

# To just run
uvicorn app:server --host 0.0.0.0
```

and the server starts listening at port 8000. Visit the base url to see the web UI in action!