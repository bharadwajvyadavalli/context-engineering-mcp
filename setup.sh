#!/bin/bash

# Setup script for Context Engineering MCP

echo "🚀 Setting up Context Engineering MCP..."

# Create project directories
echo "Creating project structure..."
mkdir -p examples/outputs
mkdir -p prompts
mkdir -p tests

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file from example
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OpenAI API key"
fi

# Run basic tests
echo "Running basic tests..."
python tests/test_basic.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Run the demo: python examples/demo.py"
echo "3. Run evaluation: python evaluate.py"
echo ""
echo "To activate the virtual environment in the future:"
echo "source venv/bin/activate"