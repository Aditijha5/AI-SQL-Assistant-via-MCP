# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install
```bash
cd AI_Sql_Assistant
python setup.py
```

This will:
- Check Python version (3.9+ required)
- Install all dependencies
- Create the database with sample data
- Set up configuration files

### Step 2: Configure API Key

Choose one method:

**Option A: Environment Variable (Recommended)**
```powershell
# PowerShell (Windows)
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# CMD (Windows)
set ANTHROPIC_API_KEY=sk-ant-...

# Linux/Mac
export ANTHROPIC_API_KEY=sk-ant-...
```

**Option B: .env File**
```bash
# Edit .env file
ANTHROPIC_API_KEY=sk-ant-...
```

Get your API key: https://console.anthropic.com/

### Step 3: Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 💬 Try These Questions

Copy and paste into the UI:

```
Show top 5 customers by total revenue
```

```
Which products sell the most and why?
```

```
What is the monthly revenue trend?
```

```
Which customers have declining purchases?
```

---

## 🧪 Test Without UI

Run the agent directly in terminal:

```bash
python agent.py
```

This runs 4 example queries and shows:
- Generated SQL
- Query results
- Business explanations

---

## 📊 Understanding the Output

### 1. Generated SQL
The AI writes SQL based on your question:
```sql
SELECT c.name, SUM(o.quantity * p.price) as revenue
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN products p ON o.product_id = p.id
GROUP BY c.id, c.name
ORDER BY revenue DESC
LIMIT 5
```

### 2. Query Results
Raw data in table format:
```
| Customer Name      | Revenue    |
|--------------------|------------|
| Acme Corporation   | $247,384   |
| TechVision Inc     | $198,221   |
```

### 3. Business Insights
AI explains what the data means:
> "The top 5 customers generate 68% of total revenue. Acme Corporation leads with consistent large orders..."

---

## 🔧 Troubleshooting

### "ANTHROPIC_API_KEY not set"
→ Follow Step 2 above to configure your API key

### "No module named 'anthropic'"
→ Run: `pip install -r requirements.txt`

### "Database not found"
→ Run: `python init_db.py`

### "Streamlit not found"
→ Run: `pip install streamlit`

### Port already in use
→ Run: `streamlit run app.py --server.port 8502`

---

## 🎯 Project Files

| File | What It Does |
|------|--------------|
| `app.py` | Streamlit web interface |
| `agent.py` | AI agent logic |
| `server.py` | MCP server (database tools) |
| `init_db.py` | Database setup |
| `db.sqlite` | Your data (created automatically) |
| `setup.py` | One-click setup script |

---

## 📚 Learn More

- **Full Documentation**: See [README.md](README.md)
- **Example Queries**: See [example_queries.md](example_queries.md)
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Claude API**: https://docs.anthropic.com/

---

## ✅ Success Checklist

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database created (`python init_db.py`)
- [ ] API key configured (`.env` or environment variable)
- [ ] Streamlit running (`streamlit run app.py`)
- [ ] Tried example queries

---

**Need help?** Check [README.md](README.md) for detailed explanations.

**Working?** You're ready to explore! Try asking your own business questions.
