#!/usr/bin/env python3
"""
Enhanced RAG with conversation memory and better UX
"""

import json
import uuid
import argparse
from typing import List, Dict
from datetime import datetime
from dataclasses import dataclass, asdict
from main import RAGSystem

@dataclass
class ConversationMessage:
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str
    sources: List[str] = None
    confidence: float = 0.0

class ConversationMemory:
    def __init__(self, max_messages: int = 10):
        self.messages: List[ConversationMessage] = []
        self.max_messages = max_messages
        self.conversation_id = str(uuid.uuid4())

    def add_message(self, role: str, content: str, sources: List[str] = None, confidence: float = 0.0):
        message = ConversationMessage(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            sources=sources or [],
            confidence=confidence
        )
        self.messages.append(message)

        # Keep only recent messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self) -> str:
        """Get formatted conversation context for RAG"""
        context_parts = []
        for msg in self.messages[-6:]:  # Last 3 exchanges
            role_display = "Human" if msg.role == "user" else "Assistant"
            context_parts.append(f"{role_display}: {msg.content}")
        return "\n\n".join(context_parts)

    def to_dict(self) -> Dict:
        return {
            "conversation_id": self.conversation_id,
            "messages": [asdict(msg) for msg in self.messages]
        }

# Enhanced RAG System with memory
class EnhancedRAGSystem(RAGSystem):
    def __init__(self):
        super().__init__()
        self.conversations: Dict[str, ConversationMemory] = {}

    def get_or_create_memory(self, conversation_id: str = None) -> ConversationMemory:
        """Get existing conversation or create new one"""
        if conversation_id and conversation_id in self.conversations:
            return self.conversations[conversation_id]

        memory = ConversationMemory()
        if conversation_id:
            memory.conversation_id = conversation_id
        # Always store the memory for future retrieval
        self.conversations[memory.conversation_id] = memory
        return memory

    def query_with_memory(self, question: str, conversation_id: str = None) -> Dict:
        """Query with conversation context"""
        memory = self.get_or_create_memory(conversation_id)

        # Add user message to memory
        memory.add_message("user", question)

        # Get conversation context
        conversation_context = memory.get_context()

        # Enhanced prompt with conversation context
        enhanced_prompt = f"""
Previous conversation:
{conversation_context}

Current question: {question}

Please provide a helpful, contextual response based on the conversation history and relevant knowledge.
"""

        # Query the knowledge base
        base_result = self.query(question)

        # Create response with context awareness
        if conversation_context and len(memory.messages) > 1:
            # Use conversation-aware model for better responses
            contextual_prompt = f"""
Based on this conversation:
{conversation_context}

And this knowledge base result: {base_result['response']}

Provide a natural, contextual response to: {question}

Keep your response conversational and helpful.
"""
            try:
                contextual_response = self.model.invoke(contextual_prompt)
                base_result['response'] = contextual_response.content
            except Exception as e:
                # Fall back to base result if contextual generation fails
                pass

        # Add assistant response to memory
        memory.add_message(
            "assistant",
            base_result['response'],
            base_result['sources'],
            base_result['confidence']
        )

        # Add conversation info to response
        base_result['conversation_id'] = memory.conversation_id
        base_result['message_count'] = len(memory.messages)

        return base_result

def main():
    parser = argparse.ArgumentParser(description="Query the enhanced RAG system with memory")
    parser.add_argument("query", help="The question to ask")
    parser.add_argument("--conversation-id", help="Conversation ID for continuity")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    rag = EnhancedRAGSystem()
    result = rag.query_with_memory(args.query, args.conversation_id)

    if args.json:
        print(json.dumps(result))
    else:
        print(f"Response: {result['response']}")
        if result['sources']:
            print(f"Sources: {result['sources']}")
        print(".2f")
        print(f"Conversation ID: {result['conversation_id']}")

if __name__ == "__main__":
    main()
