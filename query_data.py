import argparse
import json
import sys
import os
from typing import List, Tuple, Optional
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chroma"
MEMORY_FILE = "conversation_memory.json"

PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions based on the provided context from Alice in Wonderland.

Context from the book:
{context}
{conversation_context}

---

Based on the context above, answer the following question. If the context doesn't contain enough information to answer the question, say so politely.

Question: {question}

Answer:"""


def load_memory(session_id: str = "default") -> List[Tuple[str, str]]:
    """Load conversation history from memory file."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                memory = json.load(f)
                return [(item['role'], item['content']) for item in memory.get(session_id, [])]
        except (json.JSONDecodeError, KeyError):
            return []
    return []


def save_memory(session_id: str, role: str, message: str):
    """Save conversation to memory file."""
    memory = {}
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                memory = json.load(f)
        except json.JSONDecodeError:
            memory = {}
    
    if session_id not in memory:
        memory[session_id] = []
    
    memory[session_id].append({"role": role, "content": message})
    
    # Keep only last 10 messages per session
    memory[session_id] = memory[session_id][-10:]
    
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)


def query_rag(query_text: str, conversation_history: Optional[List[Tuple[str, str]]] = None) -> dict:
    """
    Query the RAG system and return structured response.
    
    Args:
        query_text: The user's question
        conversation_history: List of (role, message) tuples for context
    
    Returns:
        dict with 'answer', 'sources', 'confidence', 'error' keys
    """
    try:
        # Prepare the DB
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        # Search the DB with more results for better context
        results = db.similarity_search_with_relevance_scores(query_text, k=5)
        
        if len(results) == 0:
            return {
                "answer": "I couldn't find any relevant information in the book to answer your question.",
                "sources": [],
                "confidence": 0.0,
                "error": None
            }
        
        # Filter by relevance (lower threshold for better recall)
        filtered_results = [(doc, score) for doc, score in results if score >= 0.5]
        
        if not filtered_results:
            return {
                "answer": "I found some information, but it may not be directly relevant to your question.",
                "sources": [],
                "confidence": results[0][1] if results else 0.0,
                "error": None
            }
        
        # Build context from top results
        context_text = "\n\n---\n\n".join([
            f"[From: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}" 
            for doc, score in filtered_results[:3]
        ])
        
        # Build conversation context if provided
        conversation_context = ""
        if conversation_history:
            conv_text = "\n".join([
                f"{'Human' if role == 'user' else 'Assistant'}: {msg}"
                for role, msg in conversation_history[-3:]  # Last 3 exchanges
            ])
            conversation_context = f"\n\nPrevious conversation:\n{conv_text}\n"
        
        # Create prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            context=context_text,
            conversation_context=conversation_context,
            question=query_text
        )
        
        # Generate response
        model = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        response = model.invoke(prompt)
        response_text = response.content
        
        # Extract sources
        sources = list(set([
            doc.metadata.get("source", "Unknown") 
            for doc, _ in filtered_results[:3]
        ]))
        
        # Calculate average confidence
        avg_confidence = sum(score for _, score in filtered_results[:3]) / len(filtered_results[:3])
        
        return {
            "answer": response_text,
            "sources": sources,
            "confidence": round(avg_confidence, 2),
            "error": None
        }
        
    except Exception as e:
        return {
            "answer": None,
            "sources": [],
            "confidence": 0.0,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Query the RAG system")
    parser.add_argument("query_text", type=str, help="The query text")
    parser.add_argument("--history", type=str, help="JSON array of conversation history", default=None)
    parser.add_argument("--session-id", type=str, help="Session ID for conversation memory", default="default")
    parser.add_argument("--save-memory", action="store_true", help="Save conversation to memory file")
    args = parser.parse_args()
    
    # Parse conversation history if provided
    conversation_history = None
    if args.history:
        try:
            history_data = json.loads(args.history)
            conversation_history = [(item['role'], item['content']) for item in history_data]
        except (json.JSONDecodeError, KeyError):
            pass
    
    # Load from memory file if no history provided
    if not conversation_history:
        conversation_history = load_memory(args.session_id)
    
    # Query RAG system
    result = query_rag(args.query_text, conversation_history)
    
    # Save to memory if requested
    if args.save_memory and result.get("answer"):
        save_memory(args.session_id, "user", args.query_text)
        save_memory(args.session_id, "assistant", result["answer"])
    
    # Output as JSON for n8n to parse
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
