import argparse
import json

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def build_rag_response(query_text: str) -> dict:
    """
    Run a RAG query against the local Chroma DB and return a JSON-serializable dict.

    This is designed specifically to be easy for n8n to consume:
    {
      "answer": "<final model answer>",
      "sources": ["path/to/source.md", ...]
    }
    """
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    # If we didn't find anything useful, return a friendly fallback.
    if len(results) == 0 or results[0][1] < 0.7:
        return {
            "answer": "I couldn't find anything relevant in the knowledge base for that question.",
            "sources": [],
        }

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context_text,
        question=query_text,
    )

    # Use a deterministic model by default for more reproducible results in demos.
    model = ChatOpenAI(temperature=0)
    response_text = model.invoke(prompt).content

    sources = [doc.metadata.get("source", None) for doc, _score in results]

    return {
        "answer": response_text,
        "sources": sources,
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Simple JSON-based RAG CLI for use with n8n. "
            "Example: python rag_cli.py \"How does Alice meet the Mad Hatter?\""
        )
    )
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()

    try:
        result = build_rag_response(args.query_text)
    except Exception as exc:  # pragma: no cover - defensive, for robust demos
        # In teaching/learning scenarios we prefer a clear JSON error payload
        # over a Python stack trace on stdout.
        result = {
            "answer": "Something went wrong while answering your question.",
            "sources": [],
            "error": str(exc),
        }

    # Print a single JSON object to stdout so n8n can just JSON.parse() it.
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
