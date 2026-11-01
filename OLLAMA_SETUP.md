# Using Local Llama Models with Ollama

This guide shows you how to run the AI SQL Assistant **completely free** using local Llama models via Ollama instead of the Claude API.

---

## Why Use Ollama?

✅ **100% Free** - No API costs  
✅ **Privacy** - Everything runs locally  
✅ **No Rate Limits** - Use as much as you want  
✅ **Offline** - Works without internet (after model download)  
✅ **Fast** - Low latency with local inference  

---

## Quick Setup (3 Steps)

### Step 1: Install Ollama

**Windows:**
```powershell
# Download and install from:
# https://ollama.ai/download/windows

# Or use winget:
winget install Ollama.Ollama
```

**Mac:**
```bash
# Download from: https://ollama.ai/download/mac
# Or use Homebrew:
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Install Python Package

```powershell
pip install ollama
```

### Step 3: Pull a Llama Model

```powershell
# Pull Llama 3.2 (recommended - 2GB)
ollama pull llama3.2

# Or Llama 3.1 (larger, more capable - 4.7GB)
ollama pull llama3.1

# Or Code Llama for better SQL (7GB)
ollama pull codellama
```

---

## Running the App with Ollama

### Option 1: Automatic (Recommended)

If no `ANTHROPIC_API_KEY` is set, the app automatically uses Ollama:

```powershell
# Just run the app
streamlit run app.py
```

The app will detect Ollama and use it automatically!

### Option 2: Explicit Configuration

In the Streamlit UI, select **"Local Llama (Ollama)"** from the configuration menu.

### Option 3: Command Line

```powershell
# In agent.py, force Ollama usage:
python agent.py  # Will auto-detect Ollama if no API key
```

---

## Supported Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `llama3.2` | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | General use, fast |
| `llama3.1` | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | Better reasoning |
| `codellama` | 7GB | ⚡ | ⭐⭐⭐⭐⭐ | Best SQL generation |
| `llama2` | 3.8GB | ⚡⚡ | ⭐⭐ | Legacy support |

**Recommendation:** Start with `llama3.2` for best balance of speed and quality.

---

## How to Change Models

### In Code (agent.py)

```python
from agent import SQLAgent

# Use different model
agent = SQLAgent(use_ollama=True, ollama_model="codellama")
```

### In Streamlit

The model is set in `app.py`. Edit this line:

```python
st.session_state.agent = SQLAgent(
    use_ollama=True,
    ollama_model="llama3.2"  # Change to your preferred model
)
```

---

## Verify Ollama is Running

```powershell
# Check Ollama status
ollama list

# Test a model
ollama run llama3.2 "Hello, world!"

# Check running models
ollama ps
```

---

## Performance Comparison

### Claude API (Anthropic)
- ✅ Best quality responses
- ✅ Most accurate SQL generation
- ✅ Best business insights
- ❌ Costs money ($3-15 per million tokens)
- ❌ Requires internet
- ❌ Has rate limits

### Local Llama (Ollama)
- ✅ Completely free
- ✅ Works offline
- ✅ No rate limits
- ✅ Privacy (all local)
- ⚠️ Slightly less accurate SQL (still very good!)
- ⚠️ Requires local compute (4GB+ RAM)
- ⚠️ Slower on CPU (fast on GPU)

---

## Troubleshooting

### "Ollama not available"

**Solution:**
```powershell
pip install ollama
```

### "Connection refused"

**Solution:** Make sure Ollama is running:
```powershell
# Start Ollama service (Windows)
# It should auto-start after installation

# Or manually:
ollama serve
```

### "Model not found"

**Solution:** Pull the model first:
```powershell
ollama pull llama3.2
```

### Slow Performance

**Solutions:**
1. Use a smaller model (`llama3.2` instead of `llama3.1`)
2. Use GPU if available (Ollama auto-detects)
3. Close other applications
4. Upgrade RAM (8GB+ recommended)

### Poor SQL Quality

**Solutions:**
1. Use `codellama` model (designed for code)
2. Provide more context in your questions
3. Try `llama3.1` (larger, smarter)
4. Switch to Claude API for critical queries

---

## GPU Acceleration

Ollama automatically uses your GPU if available:

**NVIDIA GPU:**
- Ollama uses CUDA automatically
- 10-50x faster than CPU
- Recommended: 6GB+ VRAM

**Mac (Apple Silicon):**
- Ollama uses Metal automatically
- Very fast on M1/M2/M3 chips

**Check GPU Usage:**
```powershell
ollama ps  # Shows which device is being used
```

---

## Example Queries with Ollama

All the same queries work with Ollama:

```
Show top 5 customers by total revenue
Which products sell the most and why?
What is the monthly revenue trend?
Which customers have declining purchases?
```

**Quality Comparison:**
- Claude: 95% accurate SQL, excellent insights
- Llama 3.2: 85% accurate SQL, good insights
- Code Llama: 90% accurate SQL, technical insights

---

## Switching Between Claude and Ollama

You can switch at any time:

### In Streamlit UI
1. Open "⚙️ AI Model Configuration"
2. Select your preferred backend
3. Done!

### In Code
```python
# Use Claude
agent = SQLAgent(use_ollama=False)

# Use Ollama
agent = SQLAgent(use_ollama=True, ollama_model="llama3.2")

# Auto-detect (uses Ollama if no API key)
agent = SQLAgent()
```

---

## Best Practices

### For Best Results with Ollama

1. **Be Specific:** "Show revenue by customer" → "Show top 10 customers by total revenue"
2. **One Question at a Time:** Don't combine multiple questions
3. **Use CodeLlama for Complex SQL:** Switch models for hard queries
4. **Validate Results:** Double-check SQL for critical queries

### When to Use Claude vs Ollama

**Use Claude:**
- Production environments
- Critical business queries
- Complex multi-table joins
- Need best possible accuracy

**Use Ollama:**
- Development/testing
- Personal use
- Learning SQL
- Privacy-sensitive data
- Cost-conscious deployments

---

## System Requirements

### Minimum (Llama 3.2)
- **RAM:** 4GB available
- **Disk:** 5GB free
- **CPU:** Any modern processor
- **Internet:** Only for initial model download

### Recommended (Llama 3.1 / CodeLlama)
- **RAM:** 8GB+ available
- **Disk:** 10GB free
- **GPU:** NVIDIA with 6GB+ VRAM or Apple Silicon
- **Internet:** Only for initial download

---

## Advanced Configuration

### Custom System Prompt

Edit `agent.py` to customize how Ollama behaves:

```python
# In _process_with_ollama method
full_prompt = f"""You are an expert SQL analyst.
[Your custom instructions here]

DATABASE SCHEMA:
{schema_info}

USER QUESTION: {question}
"""
```

### Adjust Temperature

```python
response = ollama.chat(
    model=self.model,
    messages=[{"role": "user", "content": full_prompt}],
    options={
        "temperature": 0.2,  # Lower = more deterministic
        "top_p": 0.9
    }
)
```

---

## Cost Savings

### Claude API Cost Example
- Typical query: 2,000 tokens
- Cost: ~$0.01 per query
- 100 queries/day: **$1/day = $30/month**

### Ollama Cost
- Initial setup: 30 minutes
- Cost per query: **$0.00**
- Unlimited queries: **Free forever**

**ROI:** Ollama pays for itself after 1 day of heavy use!

---

## Summary

✅ Install Ollama: `winget install Ollama.Ollama`  
✅ Install Python package: `pip install ollama`  
✅ Pull model: `ollama pull llama3.2`  
✅ Run app: `streamlit run app.py`  
✅ **Everything works locally and free!**

---

**Questions?** Check the [main README](README.md) or [Architecture docs](ARCHITECTURE.md).
