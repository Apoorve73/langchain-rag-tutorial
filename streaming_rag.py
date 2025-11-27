#!/usr/bin/env python3
"""
Streaming RAG responses for better UX
"""

import time
import sys
import json
import argparse
from enhanced_rag import EnhancedRAGSystem

class StreamingRAGSystem(EnhancedRAGSystem):
    def stream_query(self, question: str, conversation_id: str = None):
        """Stream the RAG response"""
        memory = self.get_or_create_memory(conversation_id)
        memory.add_message("user", question)

        # First, show thinking indicator
        yield {"type": "thinking", "content": "Searching knowledge base..."}
        time.sleep(0.5)

        # Get base results
        base_result = self.query(question)

        # Stream sources first
        if base_result['sources']:
            yield {"type": "sources", "content": base_result['sources']}

        # Stream confidence
        yield {"type": "confidence", "content": ".2f"}

        # Stream response word by word
        response_words = base_result['response'].split()
        current_response = ""

        for word in response_words:
            current_response += word + " "
            yield {"type": "response", "content": current_response.strip()}
            time.sleep(0.05)  # Small delay for streaming effect

        # Add to memory
        memory.add_message("assistant", base_result['response'],
                          base_result['sources'], base_result['confidence'])

        yield {"type": "complete", "conversation_id": memory.conversation_id}

def main():
    parser = argparse.ArgumentParser(description="Stream RAG responses")
    parser.add_argument("action", choices=["stream", "query"], help="Action to perform")
    parser.add_argument("query", help="The question to ask")
    parser.add_argument("conversation_id", nargs="?", help="Conversation ID for continuity")

    args = parser.parse_args()

    rag = StreamingRAGSystem()

    if args.action == "stream":
        for chunk in rag.stream_query(args.query, args.conversation_id):
            print(json.dumps(chunk))
            sys.stdout.flush()
    elif args.action == "query":
        result = rag.query_with_memory(args.query, args.conversation_id)
        print(json.dumps(result))

if __name__ == "__main__":
    main()
