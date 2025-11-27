#!/usr/bin/env python3
"""
Automated setup script for the n8n + RAG Learning Path
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description, cwd=None):
    """Run a shell command with error handling"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {description} completed")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_dependencies():
    """Check if required tools are installed"""
    tools = ['node', 'npm']
    missing = []

    for tool in tools:
        if not shutil.which(tool):
            missing.append(tool)

    if missing:
        print(f"⚠️  Missing tools: {', '.join(missing)}")
        print("Please install Node.js from https://nodejs.org/")
        return False

    print("✅ Node.js and npm detected")
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found")
        return False

    return run_command(
        "pip install -r requirements.txt",
        "Installing Python dependencies"
    ) is not None

def install_unstructured():
    """Install unstructured with markdown support"""
    return run_command(
        'pip install "unstructured[md]"',
        "Installing unstructured markdown support"
    ) is not None

def create_env_file():
    """Create .env file if it doesn't exist"""
    if Path('.env').exists():
        print("⚠️  .env file already exists, skipping creation")
        return True

    api_key = input("Enter your OpenAI API key (or press Enter to set later): ").strip()

    env_content = f"""# OpenAI API Configuration
OPENAI_API_KEY={api_key}

# n8n Configuration (optional)
N8N_PORT=5678
N8N_HOST=localhost
"""

    with open('.env', 'w') as f:
        f.write(env_content)

    print("✅ .env file created")
    return True

def create_database():
    """Create the ChromaDB database"""
    if not Path('data/books/alice_in_wonderland.md').exists():
        print("❌ Data file not found. Please ensure data/books/alice_in_wonderland.md exists")
        return False

    return run_command(
        "python create_database.py",
        "Creating vector database"
    ) is not None

def test_rag_system():
    """Test the RAG system"""
    return run_command(
        'python main.py "Who is Alice?"',
        "Testing RAG system"
    ) is not None

def install_n8n():
    """Install n8n globally"""
    print("🔧 Installing n8n globally...")
    try:
        # Try npx first (no installation required)
        result = subprocess.run(
            "npx n8n --version",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ n8n available via npx")
            return True
    except:
        pass

    # Fall back to global installation
    choice = input("Install n8n globally? (y/n): ").lower().strip()
    if choice == 'y':
        return run_command(
            "npm install n8n -g",
            "Installing n8n globally"
        ) is not None

    print("ℹ️  You can run n8n with: npx n8n")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up n8n + RAG Learning Environment")
    print("=" * 50)

    # Pre-flight checks
    check_python_version()

    if not check_dependencies():
        sys.exit(1)

    # Install dependencies
    if not install_python_dependencies():
        sys.exit(1)

    if not install_unstructured():
        sys.exit(1)

    # Setup environment
    if not create_env_file():
        sys.exit(1)

    # Create database
    if not create_database():
        sys.exit(1)

    # Test system
    if not test_rag_system():
        print("⚠️  RAG system test failed. You may need to set your OpenAI API key in .env")
    else:
        print("🎉 RAG system is working!")

    # Install n8n
    install_n8n()

    # Final instructions
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Start n8n: npx n8n")
    print("2. Open http://localhost:5678")
    print("3. Import workflows from the workflows/ directory")
    print("4. Follow README_LEARNING.md for the complete tutorial")
    print("\nHappy learning! 🚀")

if __name__ == "__main__":
    main()
