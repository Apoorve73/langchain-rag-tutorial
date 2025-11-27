import argparse
import sys
import json
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions based on the provided context.
If the context doesn't contain enough information to answer, say so politely.

Context:
{context}

---

Question: {question}

Provide a clear, conversational answer:
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    try:
        # Check if API key exists
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Check if database exists
        if not os.path.exists(CHROMA_PATH):
            raise ValueError(f"Database not found at {CHROMA_PATH}. Please run create_database.py first.")

        # Prepare the DB
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        # Search the DB with more results and lower threshold
        results = db.similarity_search_with_relevance_scores(query_text, k=5)
        
        if len(results) == 0 or results[0][1] < 0.5:
            response = "I don't have enough information in my knowledge base to answer that question confidently."
            print(f"Response: {response}")
            print(f"Sources: []")
            return

        # Create context from top results
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results[:3]])
        
        # Generate response
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        response_text = model.invoke(prompt).content

        # Format sources with scores
        sources = [
            {
                "file": doc.metadata.get("source", "unknown"),
                "score": round(score, 2)
            }
            for doc, score in results[:3]
        ]
        
        # Output in structured format for n8n
        print(f"Response: {response_text}")
        print(f"Sources: {json.dumps(sources)}")

    except ValueError as e:
        print(f"Response: Error - {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Response: Sorry, I encountered an unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

