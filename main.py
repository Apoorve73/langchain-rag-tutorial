#!/usr/bin/env python3
"""
RAG API Wrapper for n8n Integration
Provides a clean interface for the RAG pipeline with proper error handling
"""

import sys
import json
import argparse
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Question: {question}
Answer:"""

class RAGSystem:
    def __init__(self):
        self.embedding_function = OpenAIEmbeddings()
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
        self.model = ChatOpenAI(temperature=0.1)
        self.prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    def query(self, question: str) -> dict:
        """Query the RAG system and return structured response"""
        try:
            # Search for relevant documents
            results = self.db.similarity_search_with_relevance_scores(question, k=3)

            if not results or results[0][1] < 0.7:
                return {
                    "response": "I don't have enough information in my knowledge base to answer this question accurately. Try asking about Alice in Wonderland!",
                    "sources": [],
                    "confidence": 0.0
                }

            # Prepare context and generate response
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            prompt = self.prompt_template.format(context=context_text, question=question)

            response = self.model.invoke(prompt)

            sources = [doc.metadata.get("source", "Unknown") for doc, _score in results]

            return {
                "response": response.content,
                "sources": sources,
                "confidence": float(results[0][1])
            }

        except Exception as e:
            return {
                "response": f"I encountered an error while processing your question: {str(e)}",
                "sources": [],
                "confidence": 0.0
            }

def main():
    parser = argparse.ArgumentParser(description="Query the RAG system")
    parser.add_argument("query", help="The question to ask")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    rag = RAGSystem()
    result = rag.query(args.query)

    if args.json:
        print(json.dumps(result))
    else:
        print(f"Response: {result['response']}")
        if result['sources']:
            print(f"Sources: {result['sources']}")
        print(".2f")

if __name__ == "__main__":
    main()
