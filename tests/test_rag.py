#!/usr/bin/env python3
"""
Basic tests for the RAG system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import RAGSystem
from enhanced_rag import EnhancedRAGSystem
import json

def test_basic_rag():
    """Test basic RAG functionality"""
    print("🧪 Testing basic RAG system...")

    rag = RAGSystem()

    # Test basic query
    result = rag.query("Who is Alice?")
    assert result['response'], "Should return a response"
    assert result['sources'], "Should return sources"
    assert 0.0 <= result['confidence'] <= 1.0, "Confidence should be between 0 and 1"

    print("✅ Basic RAG test passed")

def test_enhanced_rag():
    """Test enhanced RAG with memory"""
    print("🧪 Testing enhanced RAG system...")

    rag = EnhancedRAGSystem()

    # Test conversation memory
    result1 = rag.query_with_memory("Who is the Mad Hatter?")
    assert result1['conversation_id'], "Should have conversation ID"
    assert result1['message_count'] == 2, "Should have 2 messages (user + assistant)"

    # Test conversation continuity
    conversation_id = result1['conversation_id']
    result2 = rag.query_with_memory("What does he do?", conversation_id)
    assert result2['conversation_id'] == conversation_id, "Should maintain conversation ID"
    assert result2['message_count'] == 4, "Should have 4 messages now"

    print("✅ Enhanced RAG test passed")

def test_error_handling():
    """Test error handling"""
    print("🧪 Testing error handling...")

    rag = RAGSystem()

    # Test with irrelevant query
    result = rag.query("What is the weather like today?")
    assert "don't have enough information" in result['response'].lower(), "Should handle irrelevant queries"
    assert result['confidence'] < 0.5, "Should have low confidence for irrelevant queries"

    print("✅ Error handling test passed")

def test_json_output():
    """Test JSON output format"""
    print("🧪 Testing JSON output...")

    rag = RAGSystem()
    result = rag.query("Tell me about the White Rabbit")

    # Should be valid JSON
    json_str = json.dumps(result)
    parsed = json.loads(json_str)

    assert 'response' in parsed
    assert 'sources' in parsed
    assert 'confidence' in parsed

    print("✅ JSON output test passed")

def run_all_tests():
    """Run all tests"""
    print("🚀 Running RAG System Tests")
    print("=" * 40)

    try:
        test_basic_rag()
        test_enhanced_rag()
        test_error_handling()
        test_json_output()

        print("=" * 40)
        print("🎉 All tests passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
