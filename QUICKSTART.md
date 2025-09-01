# Quick Start Guide

## 1. Initial Setup (One Time)

```bash
# Clone or create the project directory
mkdir context-engineering-mcp
cd context-engineering-mcp

# Copy all the files from the artifacts

# Make setup script executable (Unix/Mac)
chmod +x setup.sh

# Run setup
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## 2. Configure OpenAI API

Edit `.env` file:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 3. Run Your First Demo

```bash
# Activate virtual environment
source venv/bin/activate

# Run simple demo
python examples/demo.py

# Run interactive demo
python examples/demo.py --mode interactive

# Run comparison demo
python examples/demo.py --mode comparison
```

## 4. Run Evaluation

```bash
# Run full evaluation suite
python evaluate.py
```

## 5. Understanding the Output

### Multi-Agent Workflow:
1. **Retriever** searches for relevant information
2. **Synthesizer** combines info into coherent response  
3. **Critic** evaluates and scores the response (1-10)
4. If score < 7, the system refines the response

### Metrics Explained:
- **Quality Score**: Critic's rating (1-10)
- **Time Overhead**: Extra time vs single agent
- **Completeness**: How well query was addressed

## 6. Customization

### Add New Test Tasks
Edit `evaluate.py`:
```python
EVALUATION_TASKS = [
    {
        "id": "custom_1",
        "query": "Your question here",
        "type": "category"
    }
]
```

### Modify Agent Prompts
Edit `prompts/agents.yaml` to change agent behaviors.

### Adjust Model Settings
Edit `.env`:
```
MODEL_NAME=gpt-4  # Use GPT-4 for better quality
MAX_TOKENS=1000    # Increase for longer responses
TEMPERATURE=0.5    # Lower for more focused responses
```

## Troubleshooting

### "API Key Invalid"
- Check your `.env` file has correct key
- Ensure no extra spaces around the key

### "Rate Limit Error"
- Add delays in `evaluate.py`
- Use fewer test tasks
- Switch to `gpt-3.5-turbo`

### "Module Not Found"
```bash
# Ensure you're in virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

## Example Output

```
Starting multi-agent workflow for query: What is quantum computing?

[1/3] Retriever Agent working...
[2/3] Synthesizer Agent working...
[3/3] Critic Agent evaluating...

✓ Workflow complete!
Quality Score: 8/10
Iterations: 1
Time: 4.3s

Final Response:
Quantum computing is a revolutionary approach to computation that leverages...
```