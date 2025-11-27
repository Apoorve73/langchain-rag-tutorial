#!/bin/bash

# RAG Chatbot Setup Script
# This script automates the setup process for the RAG chatbot project

set -e  # Exit on error

echo "🚀 RAG Chatbot Setup Script"
echo "=" | head -c 60 | tr '\n' '='
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check prerequisites
echo ""
echo "📋 Step 1: Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    print_success "Python $PYTHON_VERSION found"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version | cut -d ' ' -f 2)
    print_success "Python $PYTHON_VERSION found"
    PYTHON_CMD="python"
else
    print_error "Python not found. Please install Python 3.9+"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"
else
    print_warning "Node.js not found. You'll need it for n8n (install from nodejs.org)"
fi

# Create virtual environment
echo ""
echo "🔧 Step 2: Setting up Python virtual environment..."

if [ -d "venv" ]; then
    print_warning "Virtual environment already exists, skipping creation"
else
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Step 3: Activating virtual environment..."

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix-like systems
    source venv/bin/activate
fi

print_success "Virtual environment activated"

# Install dependencies
echo ""
echo "📦 Step 4: Installing Python dependencies..."

pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

print_success "Dependencies installed"

# Check for .env file
echo ""
echo "🔑 Step 5: Checking environment configuration..."

if [ -f ".env" ]; then
    print_success ".env file found"
    
    # Check if API key is set
    if grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
        print_success "OpenAI API key appears to be configured"
    else
        print_warning "OpenAI API key not set in .env file"
        echo ""
        echo "Please edit .env and add your OpenAI API key:"
        echo "  OPENAI_API_KEY=sk-your-key-here"
        echo ""
    fi
else
    print_warning ".env file not found, creating from template..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Created .env from .env.example"
    else
        echo "OPENAI_API_KEY=your-api-key-here" > .env
        print_success "Created .env file"
    fi
    
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your OpenAI API key:"
    echo "     nano .env  (or use your preferred editor)"
    echo ""
    
    read -p "Press Enter when you've added your API key..."
fi

# Check if data directory exists
echo ""
echo "📚 Step 6: Checking data directory..."

if [ -d "data/books" ]; then
    FILE_COUNT=$(find data/books -name "*.md" -o -name "*.txt" | wc -l)
    if [ "$FILE_COUNT" -gt 0 ]; then
        print_success "Found $FILE_COUNT document(s) in data/books/"
    else
        print_warning "No documents found in data/books/"
        echo "   Add .md or .txt files to data/books/ before creating database"
    fi
else
    print_error "data/books directory not found"
    echo "   Creating directory..."
    mkdir -p data/books
    print_success "Created data/books directory"
fi

# Create database
echo ""
echo "🗄️  Step 7: Creating vector database..."

read -p "Do you want to create/recreate the database now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "create_database_improved.py" ]; then
        $PYTHON_CMD create_database_improved.py
    else
        print_warning "create_database_improved.py not found, using original..."
        $PYTHON_CMD create_database.py
    fi
else
    print_warning "Skipping database creation"
    echo "   Run manually later: python create_database_improved.py"
fi

# Test query
echo ""
echo "🧪 Step 8: Testing RAG query..."

if [ -d "chroma" ]; then
    read -p "Do you want to test a query? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -f "query_data_improved.py" ]; then
            $PYTHON_CMD query_data_improved.py "Tell me about the content"
        else
            $PYTHON_CMD query_data.py "Tell me about the content"
        fi
    fi
else
    print_warning "Database not found, skipping test"
fi

# Final instructions
echo ""
echo "=" | head -c 60 | tr '\n' '='
echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Make sure your .env file has your OpenAI API key"
echo "2. Add documents to data/books/ (optional)"
echo "3. Run: python create_database_improved.py (if not done)"
echo "4. Install n8n: npx n8n"
echo "5. Import workflow: n8n_workflow_improved.json"
echo "6. Configure the Execute Command node with your project path"
echo ""
echo "📖 For detailed instructions, see LIGHTNING_TUTORIAL.md"
echo ""
echo "🚀 To start n8n, run: npx n8n"
echo ""

# Keep virtual environment activated
echo "💡 Virtual environment is activated. To deactivate, run: deactivate"
echo ""

