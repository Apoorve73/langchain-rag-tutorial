from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import openai 
from dotenv import load_dotenv
import os
import shutil

load_dotenv()

# Check for OpenAI API key
if not os.getenv('OPENAI_API_KEY'):
    print("❌ Error: OPENAI_API_KEY not found in environment variables")
    print("   Please create a .env file with your OpenAI API key")
    print("   Example: OPENAI_API_KEY=sk-your-key-here")
    exit(1)

openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "chroma"
DATA_PATH = "data/books"


def main():
    print("🚀 Starting database creation...")
    print("=" * 60)
    generate_data_store()
    print("=" * 60)
    print("✅ Database created successfully!")
    print("\n💡 Tip: You can now query your database with:")
    print("   python query_data.py \"Your question here\"")


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    print(f"\n📚 Step 1: Loading documents from {DATA_PATH}...")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Directory {DATA_PATH} does not exist")
        exit(1)
    
    loader = DirectoryLoader(DATA_PATH, glob="*.md", show_progress=True)
    documents = loader.load()
    
    if len(documents) == 0:
        print(f"❌ Error: No .md files found in {DATA_PATH}")
        exit(1)
    
    print(f"   ✓ Loaded {len(documents)} documents")
    
    # Show file names
    for doc in documents:
        filename = os.path.basename(doc.metadata.get('source', 'unknown'))
        print(f"     • {filename}")
    
    return documents


def split_text(documents: list[Document]):
    print(f"\n✂️  Step 2: Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  # Increased for better context
        chunk_overlap=200,  # Increased overlap
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"   ✓ Split {len(documents)} documents into {len(chunks)} chunks")
    print(f"   • Chunk size: 800 characters")
    print(f"   • Chunk overlap: 200 characters")
    
    # Show example chunk
    if len(chunks) > 0:
        print(f"\n📄 Example chunk preview:")
        example_chunk = chunks[min(10, len(chunks) - 1)]
        preview = example_chunk.page_content[:150].replace('\n', ' ')
        print(f"   \"{preview}...\"")
        print(f"   Source: {example_chunk.metadata.get('source', 'unknown')}")
    
    return chunks


def save_to_chroma(chunks: list[Document]):
    print(f"\n💾 Step 3: Saving to ChromaDB...")
    
    # Clear out the database first
    if os.path.exists(CHROMA_PATH):
        print(f"   ⚠️  Clearing existing database at {CHROMA_PATH}")
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents
    print(f"   • Creating embeddings (this may take a moment)...")
    db = Chroma.from_documents(
        chunks, 
        OpenAIEmbeddings(),
        persist_directory=CHROMA_PATH
    )
    print(f"   ✓ Saved {len(chunks)} chunks to {CHROMA_PATH}")


if __name__ == "__main__":
    main()

