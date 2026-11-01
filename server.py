"""
MCP Server for SQL Database Access
Exposes database operations as MCP tools for AI agent consumption.

Tools:
- list_tables: Returns all available tables
- describe_table: Returns schema information for a specific table
- execute_query: Executes read-only SQL queries safely
"""

import sqlite3
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Database configuration
DB_PATH = "db.sqlite"

# Initialize MCP server
app = Server("sql-assistant-mcp")


def get_db_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def is_safe_query(query: str) -> bool:
    """
    Validate that query is read-only.
    Prevents destructive operations while allowing complex SELECT statements.
    """
    query_upper = query.upper().strip()
    
    # Block any statements that modify data
    dangerous_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'TRUNCATE', 'REPLACE']
    
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            return False
    
    # Must start with SELECT or WITH (for CTEs)
    if not (query_upper.startswith('SELECT') or query_upper.startswith('WITH')):
        return False
    
    return True


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Register available MCP tools.
    These tools enable the AI to explore and query the database.
    """
    return [
        Tool(
            name="list_tables",
            description="Returns a list of all tables in the database. Use this first to understand what data is available.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="describe_table",
            description="Returns the schema (column names and types) for a specific table. Use this to understand table structure before writing queries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table to describe"
                    }
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="execute_query",
            description="Executes a read-only SQL SELECT query and returns results. Only SELECT statements are allowed. Use this to retrieve data after understanding the schema.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL SELECT query to execute"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle MCP tool invocations.
    Routes requests to appropriate database operations.
    """
    
    if name == "list_tables":
        return await handle_list_tables()
    
    elif name == "describe_table":
        table_name = arguments.get("table_name")
        if not table_name:
            return [TextContent(type="text", text="Error: table_name parameter is required")]
        return await handle_describe_table(table_name)
    
    elif name == "execute_query":
        query = arguments.get("query")
        if not query:
            return [TextContent(type="text", text="Error: query parameter is required")]
        return await handle_execute_query(query)
    
    else:
        return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]


async def handle_list_tables() -> list[TextContent]:
    """
    Return all table names in the database.
    Uses SQLite system table sqlite_master.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        result = {
            "tables": tables,
            "count": len(tables)
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error listing tables: {str(e)}"
        )]


async def handle_describe_table(table_name: str) -> list[TextContent]:
    """
    Return schema information for a specific table.
    Includes column names, types, and constraints.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get table schema using PRAGMA
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        if not columns:
            conn.close()
            return [TextContent(
                type="text",
                text=f"Error: Table '{table_name}' not found"
            )]
        
        # Format schema information
        schema = []
        for col in columns:
            col_info = {
                "name": col[1],
                "type": col[2],
                "not_null": bool(col[3]),
                "primary_key": bool(col[5])
            }
            schema.append(col_info)
        
        # Get sample row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        conn.close()
        
        result = {
            "table": table_name,
            "columns": schema,
            "row_count": row_count
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error describing table: {str(e)}"
        )]


async def handle_execute_query(query: str) -> list[TextContent]:
    """
    Execute a read-only SQL query and return results.
    Validates query safety before execution.
    """
    try:
        # Safety check
        if not is_safe_query(query):
            return [TextContent(
                type="text",
                text="Error: Only SELECT queries are allowed. Query must not contain INSERT, UPDATE, DELETE, DROP, or other modification statements."
            )]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        conn.close()
        
        # Format results
        result = {
            "query": query,
            "columns": column_names,
            "rows": rows,
            "row_count": len(rows)
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing query: {str(e)}"
        )]


async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
