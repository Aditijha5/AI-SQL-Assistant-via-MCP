"""
AI SQL Agent with MCP Integration
Orchestrates database queries using natural language understanding.

Flow:
1. User asks a business question
2. Agent calls MCP to discover database schema
3. Agent generates appropriate SQL query
4. Agent executes query via MCP
5. Agent analyzes results and provides business insights
"""

import os
import json
from typing import Dict, List, Any

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class SQLAgent:
    """
    AI agent that translates natural language to SQL using MCP tools.
    Supports both Claude API and local Llama models via Ollama.
    """
    
    def __init__(self, use_ollama=None, ollama_model="llama2:latest"):
        """Initialize the agent with either Claude API or Ollama.
        
        Args:
            use_ollama: If True, use Ollama. If False, use Claude. If None, auto-detect.
            ollama_model: Name of the Ollama model to use (default: llama3.2)
        """
        # Auto-detect if not specified
        if use_ollama is None:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            use_ollama = not api_key or not ANTHROPIC_AVAILABLE
        
        self.use_ollama = use_ollama
        
        if self.use_ollama:
            if not OLLAMA_AVAILABLE:
                raise ValueError(
                    "Ollama not available. Install with: pip install ollama\n"
                    "Also make sure Ollama is running locally."
                )
            self.client = None
            self.model = ollama_model
            print(f"✓ Using local Llama model: {ollama_model}")
        else:
            if not ANTHROPIC_AVAILABLE:
                raise ValueError("Anthropic library not available. Install with: pip install anthropic")
            
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            
            self.client = Anthropic(api_key=api_key)
            self.model = "claude-3-5-sonnet-20241022"
            print(f"✓ Using Claude API: {self.model}")
        
        # MCP tools configuration
        self.mcp_tools = self._initialize_mcp_tools()
        
        # Conversation history for context
        self.messages = []
    
    def _initialize_mcp_tools(self) -> List[Dict]:
        """
        Define MCP tools that Claude can use.
        These match the tools exposed by the MCP server.
        """
        return [
            {
                "name": "list_tables",
                "description": "Returns a list of all tables in the database. Use this first to understand what data is available.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "describe_table",
                "description": "Returns the schema (column names and types) for a specific table. Use this to understand table structure before writing queries.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Name of the table to describe"
                        }
                    },
                    "required": ["table_name"]
                }
            },
            {
                "name": "execute_query",
                "description": "Executes a read-only SQL SELECT query and returns results. Only SELECT statements are allowed.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL SELECT query to execute"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    
    def _call_mcp_tool(self, tool_name: str, tool_input: Dict) -> str:
        """
        Simulate MCP tool calls.
        In production, this would communicate with the actual MCP server.
        For this demo, we directly call the database operations.
        """
        import sqlite3
        
        db_path = "db.sqlite"
        
        try:
            if tool_name == "list_tables":
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
                tables = [row[0] for row in cursor.fetchall()]
                conn.close()
                
                result = {"tables": tables, "count": len(tables)}
                return json.dumps(result, indent=2)
            
            elif tool_name == "describe_table":
                table_name = tool_input["table_name"]
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                if not columns:
                    conn.close()
                    return f"Error: Table '{table_name}' not found"
                
                schema = []
                for col in columns:
                    schema.append({
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3]),
                        "primary_key": bool(col[5])
                    })
                
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                conn.close()
                
                result = {
                    "table": table_name,
                    "columns": schema,
                    "row_count": row_count
                }
                return json.dumps(result, indent=2)
            
            elif tool_name == "execute_query":
                query = tool_input["query"]
                
                # Safety check
                query_upper = query.upper().strip()
                dangerous_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'TRUNCATE']
                if any(keyword in query_upper for keyword in dangerous_keywords):
                    return "Error: Only SELECT queries are allowed"
                
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description] if cursor.description else []
                conn.close()
                
                result = {
                    "query": query,
                    "columns": column_names,
                    "rows": rows,
                    "row_count": len(rows)
                }
                return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """
        Main entry point: process a natural language question.
        Returns structured response with SQL, results, and explanation.
        """
        
        # System prompt that guides the agent's behavior
        system_prompt = """You are an expert SQL analyst. Your role is to help users understand their business data by:

1. First, exploring the database schema using available tools
2. Writing precise SQL queries to answer their questions
3. Explaining results in clear business language

When answering questions:
- Always start by using list_tables to see available tables
- Use describe_table to understand the schema
- Write efficient, correct SQL queries
- Provide insights, not just raw data

Important SQL patterns:
- Use JOINs to combine related data
- Use GROUP BY for aggregations
- Use ORDER BY with LIMIT for top N queries
- Calculate revenue as: quantity * price
- Format dates clearly

Be concise but thorough. Focus on business value."""

        # Add user question to conversation
        self.messages.append({
            "role": "user",
            "content": question
        })
        
        # Tracking for response
        generated_sql = None
        query_results = None
        explanation = None
        
        # Agentic loop: let AI use tools until it has an answer
        if self.use_ollama:
            # Ollama implementation (simpler, function calling via prompting)
            response_text = self._process_with_ollama(question, system_prompt)
            
            # Parse the response to extract SQL, execute, and get explanation
            generated_sql, query_results, explanation = self._parse_ollama_response(response_text, question)
            
        else:
            # Claude implementation (native tool calling)
            while True:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    system=system_prompt,
                    tools=self.mcp_tools,
                    messages=self.messages
                )
                
                # Add assistant response to conversation
                self.messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                # Check if we're done
                if response.stop_reason == "end_turn":
                    # Extract final explanation from text content
                    for block in response.content:
                        if hasattr(block, 'text'):
                            explanation = block.text
                    break
                
                # Process tool uses
                if response.stop_reason == "tool_use":
                    tool_results = []
                    
                    for block in response.content:
                        if block.type == "tool_use":
                            tool_name = block.name
                            tool_input = block.input
                            
                            # Execute the tool
                            result = self._call_mcp_tool(tool_name, tool_input)
                            
                            # Track SQL queries and results
                            if tool_name == "execute_query":
                                generated_sql = tool_input.get("query")
                                try:
                                    query_results = json.loads(result)
                                except:
                                    query_results = {"error": result}
                            
                            # Add tool result to conversation
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result
                            })
                    
                    # Continue conversation with tool results
                    self.messages.append({
                        "role": "user",
                        "content": tool_results
                    })
        
        return {
            "sql": generated_sql,
            "results": query_results,
            "explanation": explanation
        }
    
    def _process_with_ollama(self, question: str, system_prompt: str) -> str:
        """Process question using Ollama (local Llama model)."""
        # Get database schema first
        tables = self._call_mcp_tool("list_tables", {})
        
        schema_info = []
        tables_list = json.loads(tables).get("tables", [])
        for table in tables_list:
            schema = self._call_mcp_tool("describe_table", {"table_name": table})
            schema_data = json.loads(schema)
            
            # Format schema more clearly
            columns = ", ".join([f"{col['name']} ({col['type']})" for col in schema_data['columns']])
            schema_info.append(f"{table}: {columns}")
        
        # Build comprehensive prompt for Llama with clear schema
        full_prompt = f"""You are an expert SQL analyst. Write a SQL query to answer the user's question.

DATABASE TABLES:
{chr(10).join(schema_info)}

IMPORTANT RULES:
- Use exact column names from the schema above
- The products table has: id, name, price
- The orders table has: id, customer_id, product_id, quantity, order_date
- The customers table has: id, name, country
- To calculate revenue: multiply quantity * price
- Use table aliases: c for customers, o for orders, p for products
- For "top N" queries, always include ORDER BY and LIMIT N
- Sort descending (DESC) for "top" or "highest", ascending (ASC) for "bottom" or "lowest"
- Test your query mentally before writing it

USER QUESTION: {question}

Provide ONLY the SQL query in a code block, followed by a brief explanation.

Format:
```sql
[SQL query here]
```

EXPLANATION:
[Brief analysis]
"""
        
        # Call Ollama with lower temperature for more consistent SQL
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": full_prompt}],
            options={"temperature": 0.2}
        )
        
        return response['message']['content']
    
    def _parse_ollama_response(self, response_text: str, question: str) -> tuple:
        """Parse Ollama response to extract SQL and explanation."""
        generated_sql = None
        query_results = None
        explanation = response_text
        
        # Extract SQL from code blocks
        if "```sql" in response_text:
            sql_start = response_text.find("```sql") + 6
            sql_end = response_text.find("```", sql_start)
            if sql_end > sql_start:
                generated_sql = response_text[sql_start:sql_end].strip()
        elif "```" in response_text:
            # Try generic code block
            sql_start = response_text.find("```") + 3
            sql_end = response_text.find("```", sql_start)
            if sql_end > sql_start:
                potential_sql = response_text[sql_start:sql_end].strip()
                if potential_sql.upper().startswith("SELECT"):
                    generated_sql = potential_sql
        
        # Execute the query if we found SQL
        if generated_sql:
            result = self._call_mcp_tool("execute_query", {"query": generated_sql})
            try:
                query_results = json.loads(result)
            except:
                query_results = {"error": result}
        
        # Extract explanation (text after EXPLANATION: or after SQL block)
        if "EXPLANATION:" in response_text:
            explanation = response_text.split("EXPLANATION:")[1].strip()
        elif "```" in response_text:
            # Get text after last code block
            last_block_end = response_text.rfind("```") + 3
            explanation = response_text[last_block_end:].strip()
        
        return generated_sql, query_results, explanation
    
    def reset_conversation(self):
        """Clear conversation history for new question."""
        self.messages = []


def demo():
    """
    Demonstration of the AI SQL Agent.
    Shows example questions and how the agent handles them.
    """
    print("=== AI SQL Agent Demo ===\n")
    
    # Initialize agent
    agent = SQLAgent()
    
    # Example questions
    questions = [
        "Show top 5 customers by total revenue",
        "Which products sell the most and why?",
        "What is the monthly revenue trend?",
        "Which customers have declining purchases?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"Question {i}: {question}")
        print('='*60)
        
        agent.reset_conversation()
        response = agent.process_question(question)
        
        # Display SQL
        if response['sql']:
            print("\n📊 Generated SQL:")
            print(response['sql'])
        
        # Display results
        if response['results']:
            print("\n📋 Query Results:")
            if 'columns' in response['results']:
                print(f"Columns: {', '.join(response['results']['columns'])}")
                print(f"Rows returned: {response['results']['row_count']}")
                if response['results']['rows']:
                    print("\nSample data:")
                    for row in response['results']['rows'][:5]:
                        print(row)
        
        # Display explanation
        if response['explanation']:
            print("\n💡 Business Insight:")
            print(response['explanation'])


if __name__ == "__main__":
    demo()
