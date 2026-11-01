# System Architecture

## Overview

This document explains how the AI SQL Assistant works at a technical level.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                        USER                               │
└────────────────────────┬─────────────────────────────────┘
                         │
                         │ Natural Language Question
                         │ "Show top 5 customers by revenue"
                         ▼
┌──────────────────────────────────────────────────────────┐
│                   STREAMLIT UI (app.py)                   │
│  ┌────────────────────────────────────────────────────┐  │
│  │  • Text input box                                  │  │
│  │  • Run Query button                                │  │
│  │  • Results display (SQL, Table, Insights)          │  │
│  └────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────┘
                         │
                         │ Forward question
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  AI AGENT (agent.py)                      │
│  ┌────────────────────────────────────────────────────┐  │
│  │  SQLAgent Class                                    │  │
│  │  • Manages conversation with Claude                │  │
│  │  • Defines MCP tools                               │  │
│  │  • Orchestrates workflow                           │  │
│  └────────────────────────────────────────────────────┘  │
│                         │                                 │
│                         │ Calls Claude API                │
│                         ▼                                 │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Claude 3.5 Sonnet (Anthropic API)                │  │
│  │  • Understands user intent                         │  │
│  │  • Decides which MCP tools to use                  │  │
│  │  • Generates SQL queries                           │  │
│  │  • Analyzes results                                │  │
│  └────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────┘
                         │
                         │ MCP Tool Calls
                         ▼
┌──────────────────────────────────────────────────────────┐
│              MCP TOOL EXECUTOR (agent.py)                 │
│  ┌────────────────────────────────────────────────────┐  │
│  │  _call_mcp_tool() method                           │  │
│  │  • Receives tool name + parameters                 │  │
│  │  • Routes to appropriate database operation        │  │
│  │  • Returns JSON results                            │  │
│  └────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────┘
                         │
                         │ SQL Commands
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  DATABASE (db.sqlite)                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  customers      │  orders       │  products        │  │
│  │  ─────────      │  ──────       │  ────────        │  │
│  │  • id           │  • id          │  • id            │  │
│  │  • name         │  • customer_id │  • name          │  │
│  │  • country      │  • product_id  │  • price         │  │
│  │                 │  • quantity    │                  │  │
│  │  15 rows        │  • order_date  │  10 rows         │  │
│  │                 │  395 rows      │                  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Streamlit UI (`app.py`)

**Responsibilities:**
- User interface and interaction
- Display results in clean format
- Handle API key configuration

**Key Functions:**
```python
render_query_input()      # Question input box
process_query()           # Send to agent
render_sql_section()      # Show generated SQL
render_results_section()  # Display data table
render_explanation_section()  # Business insights
```

**Data Flow:**
1. User enters question
2. Calls `agent.process_question(question)`
3. Receives structured response
4. Renders SQL, results, and explanation

---

### 2. AI Agent (`agent.py`)

**Responsibilities:**
- Orchestrate AI-database interaction
- Manage Claude API communication
- Execute MCP tool calls
- Structure responses

**Key Class: SQLAgent**

```python
class SQLAgent:
    def __init__(self):
        # Initialize Anthropic client
        # Define MCP tools
        # Setup conversation tracking
    
    def process_question(self, question: str) -> Dict:
        # Main workflow:
        # 1. Send question to Claude
        # 2. Claude decides to use tools
        # 3. Execute tool calls
        # 4. Return results to Claude
        # 5. Claude generates final response
        # 6. Return structured output
    
    def _call_mcp_tool(self, tool_name: str, tool_input: Dict) -> str:
        # Route to appropriate database operation
        # Execute safely
        # Return JSON results
```

**Agentic Loop:**
```
User Question
    ↓
Claude receives question
    ↓
Claude: "I need to see tables" → calls list_tables
    ↓
Agent executes → returns table list
    ↓
Claude: "I need schema" → calls describe_table
    ↓
Agent executes → returns columns/types
    ↓
Claude: "I'll query the data" → calls execute_query
    ↓
Agent executes SQL → returns results
    ↓
Claude: "Here's what this means" → generates explanation
    ↓
Agent returns complete response
```

---

### 3. MCP Tools

**Three core tools exposed to Claude:**

#### Tool 1: `list_tables`
```json
{
  "name": "list_tables",
  "description": "Returns all tables in database",
  "input_schema": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```

**Returns:**
```json
{
  "tables": ["customers", "orders", "products"],
  "count": 3
}
```

#### Tool 2: `describe_table`
```json
{
  "name": "describe_table",
  "description": "Returns schema for a table",
  "input_schema": {
    "type": "object",
    "properties": {
      "table_name": {"type": "string"}
    },
    "required": ["table_name"]
  }
}
```

**Returns:**
```json
{
  "table": "customers",
  "columns": [
    {"name": "id", "type": "INTEGER", "primary_key": true},
    {"name": "name", "type": "TEXT", "not_null": true},
    {"name": "country", "type": "TEXT", "not_null": true}
  ],
  "row_count": 15
}
```

#### Tool 3: `execute_query`
```json
{
  "name": "execute_query",
  "description": "Executes read-only SQL query",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"}
    },
    "required": ["query"]
  }
}
```

**Returns:**
```json
{
  "query": "SELECT name, country FROM customers LIMIT 5",
  "columns": ["name", "country"],
  "rows": [
    ["Acme Corporation", "USA"],
    ["TechVision Inc", "USA"]
  ],
  "row_count": 5
}
```

---

### 4. MCP Server (`server.py`)

**Note:** In this implementation, the MCP server is defined but not actively used in stdio mode. The agent directly calls database operations for simplicity.

**Purpose (for future expansion):**
- Run as standalone process
- Communicate via stdio/HTTP
- Enable multi-client access
- Centralize database logic

**Implementation:**
```python
@app.list_tools()
async def list_tools():
    # Register available tools
    
@app.call_tool()
async def call_tool(name, arguments):
    # Route tool calls to handlers
    
async def handle_execute_query(query):
    # Validate query safety
    # Execute against database
    # Return results
```

---

### 5. Database (`db.sqlite`)

**Schema:**

```sql
-- Customers (15 records)
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL
);

-- Products (10 records)
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

-- Orders (395 records)
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Data Characteristics:**
- **Realistic**: B2B company names, product names, pricing
- **Varied**: Different purchase patterns (heavy/medium/light buyers)
- **Temporal**: 12 months of transaction history
- **Patterns**: Includes trends, seasonality, churn signals

---

## Data Flow: Complete Example

### User Question
```
"Show top 5 customers by total revenue"
```

### Step-by-Step Flow

**1. UI receives question** (`app.py`)
```python
process_query("Show top 5 customers by total revenue")
```

**2. Agent sends to Claude** (`agent.py`)
```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Show top 5..."}],
    tools=[list_tables, describe_table, execute_query]
)
```

**3. Claude decides: "I need schema first"**
```json
{
  "type": "tool_use",
  "name": "list_tables",
  "input": {}
}
```

**4. Agent executes tool**
```python
result = _call_mcp_tool("list_tables", {})
# Returns: {"tables": ["customers", "orders", "products"], "count": 3}
```

**5. Claude analyzes, calls next tool**
```json
{
  "type": "tool_use",
  "name": "describe_table",
  "input": {"table_name": "customers"}
}
```

**6. Agent executes**
```python
result = _call_mcp_tool("describe_table", {"table_name": "customers"})
# Returns schema information
```

**7. Claude repeats for other tables**
```json
describe_table("orders")
describe_table("products")
```

**8. Claude generates SQL**
```json
{
  "type": "tool_use",
  "name": "execute_query",
  "input": {
    "query": "SELECT c.name, SUM(o.quantity * p.price) as revenue 
              FROM customers c 
              JOIN orders o ON c.id = o.customer_id 
              JOIN products p ON o.product_id = p.id 
              GROUP BY c.id ORDER BY revenue DESC LIMIT 5"
  }
}
```

**9. Agent executes query**
```python
result = _call_mcp_tool("execute_query", {"query": "SELECT..."})
# Returns: {"columns": [...], "rows": [...], "row_count": 5}
```

**10. Claude analyzes results**
```json
{
  "type": "text",
  "text": "The top 5 customers by revenue are:
           1. Acme Corporation ($247,384)
           2. TechVision Inc ($198,221)
           ...
           These customers represent 68% of total revenue..."
}
```

**11. Agent structures response**
```python
return {
    "sql": "SELECT c.name, SUM...",
    "results": {"columns": [...], "rows": [...]},
    "explanation": "The top 5 customers..."
}
```

**12. UI displays all sections**
- SQL in code block
- Results in table
- Explanation as text

---

## Security Architecture

### Query Validation

**Multi-layer protection:**

1. **Keyword Blocking**
```python
dangerous_keywords = [
    'INSERT', 'UPDATE', 'DELETE', 'DROP', 
    'ALTER', 'CREATE', 'TRUNCATE', 'REPLACE'
]
```

2. **Statement Type Check**
```python
if not (query.startswith('SELECT') or query.startswith('WITH')):
    return "Error: Only SELECT queries allowed"
```

3. **Execution Isolation**
```python
# Read-only connection
conn = sqlite3.connect('db.sqlite')
# No commit() calls
```

**Result:** Even if AI generates unsafe SQL, it cannot execute.

---

## Performance Considerations

### Optimization Points

1. **Connection Pooling** (future)
   - Currently: New connection per query
   - Future: Connection pool for concurrent requests

2. **Query Caching** (future)
   - Store recent query results
   - Avoid re-execution of identical queries

3. **Schema Caching**
   - Currently: Re-fetch schema each time
   - Future: Cache schema, invalidate on changes

4. **Streaming Results** (future)
   - For large result sets
   - Progressive rendering in UI

### Current Performance
- **Small DB (400 rows)**: < 1 second per query
- **Claude API**: 2-5 seconds for reasoning
- **Total Response Time**: 3-7 seconds typical

---

## Extension Points

### Easy Extensions

1. **Add New Tools**
```python
# In agent.py
mcp_tools.append({
    "name": "export_to_excel",
    "description": "Export query results to Excel",
    "input_schema": {...}
})
```

2. **Multi-Database Support**
```python
# Add PostgreSQL/MySQL connectors
if db_type == "postgres":
    conn = psycopg2.connect(...)
elif db_type == "mysql":
    conn = mysql.connector.connect(...)
```

3. **Query History**
```python
# Store in SQLite
CREATE TABLE query_history (
    id INTEGER PRIMARY KEY,
    question TEXT,
    sql TEXT,
    timestamp TEXT
);
```

4. **Visualization**
```python
# In app.py
import plotly.express as px

if response['results']:
    df = pd.DataFrame(response['results']['rows'])
    fig = px.bar(df, x=df.columns[0], y=df.columns[1])
    st.plotly_chart(fig)
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| AI | Claude 3.5 Sonnet | Natural language understanding, SQL generation |
| Protocol | MCP | Tool definition and execution |
| Backend | Python 3.9+ | Core logic |
| Database | SQLite 3 | Data storage |
| UI | Streamlit | Web interface |
| API | Anthropic API | Claude access |

---

## Files and Responsibilities

```
AI_Sql_Assistant/
│
├── app.py                    # UI layer
│   ├── render_*() functions  # Display components
│   └── process_query()       # Coordination
│
├── agent.py                  # Business logic layer
│   ├── SQLAgent class        # Main orchestrator
│   ├── process_question()    # Workflow engine
│   └── _call_mcp_tool()      # MCP execution
│
├── server.py                 # MCP server (optional)
│   ├── @app.list_tools()     # Tool registration
│   └── @app.call_tool()      # Tool handler
│
├── init_db.py                # Data layer
│   └── create_database()     # Schema + seed data
│
└── db.sqlite                 # Storage layer
    └── [customers, orders, products]
```

---

## Future Architecture

### Proposed Enhancements

```
┌──────────────────────────────────────────────────────────┐
│                    Web UI (React)                         │
│                  Mobile App (React Native)                │
│                  Slack Bot / Teams Bot                    │
└────────────────────────┬─────────────────────────────────┘
                         │
                         │ REST API / WebSocket
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  API Gateway (FastAPI)                    │
│  • Authentication (JWT)                                   │
│  • Rate limiting                                          │
│  • Request routing                                        │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  Agent Pool (Redis Queue)                 │
│  • Load balancing                                         │
│  • Query queue management                                 │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│              MCP Server (Standalone Process)              │
│  • stdio/HTTP transport                                   │
│  • Connection pooling                                     │
│  • Query caching                                          │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│          Database Layer (PostgreSQL/MySQL)                │
│  • Read replicas                                          │
│  • Query optimization                                     │
│  • Audit logging                                          │
└──────────────────────────────────────────────────────────┘
```

---

**This architecture balances simplicity with extensibility—easy to understand today, easy to scale tomorrow.**
