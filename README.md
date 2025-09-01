# Context Engineering MCP

A simple multi-agent system where specialized LLM agents collaborate to solve problems through structured communication.

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Quick Start

Run a simple demo:
```bash
python examples/demo.py
```

Run evaluation:
```bash
python evaluate.py
```

## Architecture

Three specialized agents work together:
- **Retriever**: Gathers relevant information
- **Synthesizer**: Combines information into coherent responses  
- **Critic**: Evaluates outputs for quality and accuracy

## Project Structure
```
├── agents.py           # Agent implementations
├── messages.py         # Message protocol
├── workflow.py         # Orchestration logic
├── evaluate.py         # Evaluation script
├── examples/
│   └── demo.py        # Simple demonstration
└── prompts/
    └── agents.yaml    # Agent prompt templates
```