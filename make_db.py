from chromadb import EmbeddingFunction
from chromadb.utils import embedding_functions
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from typing import List, Sequence

import logging
import sys

# PDF not provided, choose your own
PDF_PATH = "book.pdf"

lg = logging.getLogger(__name__)
logging.basicConfig(
    format = "%(name)15s - %(levelname)5s: %(message)s",
    level = logging.DEBUG,
)

lg.info(f"Loading PDF: {PDF_PATH}")

loader = PyPDFLoader(PDF_PATH)
pages = loader.load_and_split()

lg.info("Creating model for embedding")

# Might want a different embedding function for better performance
embed_fn = embedding_functions.DefaultEmbeddingFunction()

if embed_fn is None:
    lg.error("No default embedding function, quitting")
    sys.exit(1)

class Helper:
    def __init__(self, embed_fn: EmbeddingFunction):
        self.embed_fn = embed_fn

    def embed_query(self, text: str) -> Sequence[float]:
        embed_doc_result = self.embed_documents([text])
        if len(embed_doc_result) < 1:
            lg.error(
                "Embedding empty in result of `embed_query`, should " +
                "produce `IndexError`."
            )
        if len(embed_doc_result) > 1:
            lg.warn(
                "More than one embedding in result of `embed_query`, " +
                "taking first"
            )
        return embed_doc_result[0]

    def embed_documents(self, texts: List[str]) -> List[Sequence[float]]:
        return self.embed_fn(texts)

model = Helper(embed_fn)
pages_content = [page.page_content for page in pages]

lg.info(f"Creating ChromaDB from documents")

db = Chroma.from_documents(
    pages,
    # The typing is inaccurate here
    embedding = model,
    persist_directory = "./chromadb",
)

lg.info("Finished creating ChromaDB")

# query the db
query = "Is the square root of 2 real?"
docs = db.similarity_search(query, k = 3)

# print results
print([doc.page_content for doc in docs])
