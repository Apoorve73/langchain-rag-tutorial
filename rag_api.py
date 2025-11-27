"""
RAG API Server - Provides HTTP endpoint for n8n integration
Run with: python rag_api.py

This server provides a REST API for querying the Alice in Wonderland
knowledge base using RAG (Retrieval-Augmented Generation).
"""
from flask import Flask, request, jsonify
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CHROMA_PATH = "chroma"

# Conversation memory (keeps last 5 exchanges for context)
memory = ConversationBufferWindowMemory(k=5, return_messages=True)

PROMPT_TEMPLATE = """You are a helpful and friendly assistant that answers questions about Alice in Wonderland.
Use the following context from the book to answer the question accurately and engagingly.
If you cannot find the answer in the context, say so honestly but suggest related topics you could help with.

Context from the book:
{context}

Previous conversation:
{history}

User's question: {question}

Provide a helpful, conversational response:"""


def get_rag_response(query: str) -> dict:
    """
    Get RAG response with sources and confidence score.
    
    Args:
        query: The user's question
        
    Returns:
        dict with response, sources, and confidence
    """
    try:
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        # Search for relevant chunks (top 3)
        results = db.similarity_search_with_relevance_scores(query, k=3)
        
        if len(results) == 0 or results[0][1] < 0.5:
            logger.info(f"No relevant results found for query: {query}")
            return {
                "response": "I couldn't find relevant information about that in Alice in Wonderland. "
                           "Try asking about specific characters like the Mad Hatter, Cheshire Cat, "
                           "or Queen of Hearts, or events like the tea party or the croquet game!",
                "sources": [],
                "confidence": 0
            }
        
        # Build context from retrieved chunks
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        
        # Get conversation history
        history = memory.load_memory_variables({}).get("history", "No previous conversation")
        
        # Generate response using OpenAI
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            context=context_text, 
            history=history,
            question=query
        )
        
        model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        response_text = model.invoke(prompt).content
        
        # Update conversation memory
        memory.save_context({"input": query}, {"output": response_text})
        
        # Extract unique sources
        sources = list(set([doc.metadata.get("source", "unknown") for doc, _ in results]))
        
        # Calculate average confidence score
        avg_score = sum([score for _, score in results]) / len(results)
        
        logger.info(f"Query: {query} | Confidence: {avg_score:.2f}")
        
        return {
            "response": response_text,
            "sources": sources,
            "confidence": round(avg_score, 2)
        }
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return {
            "response": f"Sorry, I encountered an error processing your question. Please try again.",
            "sources": [],
            "confidence": 0,
            "error": str(e)
        }


@app.route("/query", methods=["POST"])
def query():
    """
    Handle RAG queries via HTTP POST.
    
    Expected JSON body:
    {
        "question": "Your question here"
    }
    
    Returns:
    {
        "response": "The AI-generated answer",
        "sources": ["list", "of", "sources"],
        "confidence": 0.85
    }
    """
    data = request.get_json()
    
    if not data or "question" not in data:
        return jsonify({
            "error": "Missing 'question' in request body",
            "example": {"question": "Who is the Mad Hatter?"}
        }), 400
    
    question = data["question"].strip()
    
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400
    
    result = get_rag_response(question)
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "service": "rag-api",
        "version": "1.0.0"
    })


@app.route("/reset", methods=["POST"])
def reset_memory():
    """Reset conversation memory to start fresh."""
    global memory
    memory = ConversationBufferWindowMemory(k=5, return_messages=True)
    logger.info("Conversation memory reset")
    return jsonify({"status": "memory cleared", "message": "Ready for a new conversation!"})


@app.route("/", methods=["GET"])
def home():
    """Root endpoint with API documentation."""
    return jsonify({
        "service": "Alice in Wonderland RAG API",
        "version": "1.0.0",
        "endpoints": {
            "POST /query": "Send a question to get an AI-generated answer",
            "GET /health": "Check if the service is running",
            "POST /reset": "Clear conversation memory"
        },
        "example": {
            "endpoint": "POST /query",
            "body": {"question": "Who is the Cheshire Cat?"}
        }
    })


if __name__ == "__main__":
    print("=" * 50)
    print("🐰 Alice in Wonderland RAG API")
    print("=" * 50)
    print("Starting server on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  POST /query  - Ask questions about Alice in Wonderland")
    print("  GET  /health - Health check")
    print("  POST /reset  - Clear conversation memory")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)

