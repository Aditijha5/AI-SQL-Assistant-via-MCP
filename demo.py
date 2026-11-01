"""
Demo Script for AI SQL Assistant
Use this to showcase the project's capabilities in presentations or interviews.
"""

import os
import sys


def print_section(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def demo_introduction():
    """Introduce the project."""
    print_section("AI SQL Assistant - Live Demo")
    
    print("This demonstration shows how an AI agent uses the Model Context Protocol")
    print("(MCP) to interact with a database intelligently.\n")
    
    print("Key Features:")
    print("  • Natural language to SQL translation")
    print("  • Automatic schema discovery")
    print("  • Business intelligence analysis")
    print("  • Production-quality code architecture\n")
    
    input("Press Enter to continue...")


def demo_architecture():
    """Explain the architecture."""
    print_section("System Architecture")
    
    print("┌─────────────┐")
    print("│  Streamlit  │  ← User asks business questions")
    print("└──────┬──────┘")
    print("       │")
    print("       ▼")
    print("┌─────────────┐")
    print("│  AI Agent   │  ← Claude 3.5 with MCP tools")
    print("└──────┬──────┘")
    print("       │")
    print("       ▼")
    print("┌─────────────┐")
    print("│ MCP Server  │  ← Exposes database operations")
    print("└──────┬──────┘")
    print("       │")
    print("       ▼")
    print("┌─────────────┐")
    print("│   SQLite    │  ← Business data")
    print("└─────────────┘\n")
    
    print("Flow:")
    print("1. User: 'Show top 5 customers by revenue'")
    print("2. AI calls MCP tools to explore database schema")
    print("3. AI generates optimized SQL query")
    print("4. AI executes query safely (read-only)")
    print("5. AI explains results in business language\n")
    
    input("Press Enter to continue...")


def demo_database():
    """Show database structure."""
    print_section("Database Overview")
    
    import sqlite3
    
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    
    # Show tables
    print("Tables:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for row in cursor.fetchall():
        print(f"  • {row[0]}")
    
    print("\nSchema:")
    print("  customers(id, name, country)")
    print("  products(id, name, price)")
    print("  orders(id, customer_id, product_id, quantity, order_date)")
    
    # Show counts
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]
    
    print(f"\nData Volume:")
    print(f"  • {customer_count} customers across 8 countries")
    print(f"  • {product_count} B2B products ($599 - $12,999)")
    print(f"  • {order_count} orders over 12 months")
    
    # Show sample data
    print("\nSample Customers:")
    cursor.execute("SELECT name, country FROM customers LIMIT 5")
    for row in cursor.fetchall():
        print(f"  • {row[0]} ({row[1]})")
    
    print("\nSample Products:")
    cursor.execute("SELECT name, price FROM products LIMIT 5")
    for row in cursor.fetchall():
        print(f"  • {row[0]}: ${row[1]:,.2f}")
    
    conn.close()
    
    input("\nPress Enter to continue...")


def demo_example_queries():
    """Show example queries the system can handle."""
    print_section("Example Queries")
    
    examples = [
        ("Revenue Analysis", "Show top 5 customers by total revenue"),
        ("Product Performance", "Which products sell the most and why?"),
        ("Trend Analysis", "What is the monthly revenue trend?"),
        ("Customer Health", "Which customers have declining purchases?"),
        ("Geographic Insights", "What countries generate the most revenue?"),
        ("Order Analytics", "Show average order value by customer"),
        ("Product Strategy", "Which products have the highest profit margins?"),
        ("Seasonal Patterns", "Analyze seasonal trends in orders")
    ]
    
    print("The AI can answer complex business questions like:\n")
    
    for i, (category, question) in enumerate(examples, 1):
        print(f"{i}. {category}")
        print(f"   \"{question}\"\n")
    
    input("Press Enter to continue...")


def demo_ai_workflow():
    """Explain how the AI processes questions."""
    print_section("AI Workflow Example")
    
    print("Question: \"Show top 5 customers by total revenue\"\n")
    
    print("Step 1: AI calls list_tables")
    print("  → Returns: ['customers', 'orders', 'products']\n")
    
    print("Step 2: AI calls describe_table('customers')")
    print("  → Returns: {id, name, country}\n")
    
    print("Step 3: AI calls describe_table('orders')")
    print("  → Returns: {id, customer_id, product_id, quantity, order_date}\n")
    
    print("Step 4: AI calls describe_table('products')")
    print("  → Returns: {id, name, price}\n")
    
    print("Step 5: AI generates SQL")
    print("  SELECT c.name, SUM(o.quantity * p.price) as revenue")
    print("  FROM customers c")
    print("  JOIN orders o ON c.id = o.customer_id")
    print("  JOIN products p ON o.product_id = p.id")
    print("  GROUP BY c.id, c.name")
    print("  ORDER BY revenue DESC")
    print("  LIMIT 5\n")
    
    print("Step 6: AI executes query and receives results\n")
    
    print("Step 7: AI analyzes and explains")
    print("  \"The top 5 customers generate 68% of total revenue.")
    print("   Acme Corporation leads with $247,384, driven by")
    print("   consistent Enterprise Software purchases...\"\n")
    
    input("Press Enter to continue...")


def demo_security():
    """Explain security features."""
    print_section("Security & Safety")
    
    print("Read-Only Queries:")
    print("  • Blocks INSERT, UPDATE, DELETE, DROP")
    print("  • Only SELECT statements allowed")
    print("  • Validates query syntax before execution\n")
    
    print("Example - Dangerous Query Blocked:")
    print("  ❌ DROP TABLE customers")
    print("  ❌ DELETE FROM orders")
    print("  ❌ UPDATE products SET price = 0")
    print("  ✓ SELECT * FROM customers\n")
    
    print("Safety Features:")
    print("  • SQL injection prevention")
    print("  • No schema modifications")
    print("  • No data manipulation")
    print("  • Isolated database connection\n")
    
    input("Press Enter to continue...")


def demo_code_quality():
    """Highlight code quality aspects."""
    print_section("Code Quality Highlights")
    
    print("Production-Grade Design:")
    print("  • Clean, readable code with minimal complexity")
    print("  • Comprehensive docstrings explaining 'why'")
    print("  • Type hints for better IDE support")
    print("  • Error handling throughout\n")
    
    print("Enterprise Patterns:")
    print("  • Separation of concerns (UI / Agent / Database)")
    print("  • Configuration via environment variables")
    print("  • Structured logging and validation")
    print("  • Modular, testable components\n")
    
    print("Developer Experience:")
    print("  • One-command setup (setup.py)")
    print("  • Automated testing (test_system.py)")
    print("  • Clear documentation (README, ARCHITECTURE)")
    print("  • Example queries and tutorials\n")
    
    input("Press Enter to continue...")


def demo_mcp_benefits():
    """Explain MCP advantages."""
    print_section("Why Model Context Protocol (MCP)?")
    
    print("Without MCP:")
    print("  • Hardcode database schema in prompts")
    print("  • Manual query execution and parsing")
    print("  • Difficult to update when schema changes")
    print("  • AI has no way to explore dynamically\n")
    
    print("With MCP:")
    print("  ✓ AI discovers schema automatically")
    print("  ✓ Dynamic tool invocation")
    print("  ✓ Schema changes don't require prompt updates")
    print("  ✓ AI can explore and reason about data")
    print("  ✓ Standardized protocol for tool calling\n")
    
    print("Key Insight:")
    print("  The AI has never seen this database before.")
    print("  It learns the structure on-the-fly using MCP tools,")
    print("  just like a human analyst would.\n")
    
    input("Press Enter to continue...")


def demo_use_cases():
    """Show real-world applications."""
    print_section("Real-World Use Cases")
    
    print("This architecture enables:\n")
    
    print("1. Internal BI Tool")
    print("   • Non-technical staff query databases")
    print("   • Reduce SQL knowledge requirement")
    print("   • Faster data access for decisions\n")
    
    print("2. Customer Support")
    print("   • Query order history naturally")
    print("   • \"Show all orders from customer X last month\"")
    print("   • Instant insights without dashboards\n")
    
    print("3. Executive Reporting")
    print("   • Ad-hoc analysis without analysts")
    print("   • \"Compare Q1 vs Q2 revenue by region\"")
    print("   • Self-service intelligence\n")
    
    print("4. Data Exploration")
    print("   • Understand new datasets quickly")
    print("   • \"What patterns exist in customer churn?\"")
    print("   • AI-guided analysis\n")
    
    input("Press Enter to continue...")


def demo_extensions():
    """Suggest future enhancements."""
    print_section("Extension Possibilities")
    
    print("Easy to Add:")
    print("  • Chart generation (Plotly/Matplotlib)")
    print("  • Export to Excel/PDF")
    print("  • Query history and favorites")
    print("  • Multi-database support (PostgreSQL, MySQL)")
    print("  • Scheduled reports via email\n")
    
    print("Advanced Features:")
    print("  • Voice interface ('Alexa, show top customers')")
    print("  • Slack/Teams bot integration")
    print("  • Real-time data refresh")
    print("  • Collaborative query sharing")
    print("  • AI-suggested analyses\n")
    
    print("Enterprise Ready:")
    print("  • SSO authentication")
    print("  • Role-based access control")
    print("  • Audit logging")
    print("  • Multi-tenant architecture")
    print("  • High availability setup\n")
    
    input("Press Enter to continue...")


def demo_conclusion():
    """Wrap up the demonstration."""
    print_section("Summary")
    
    print("What We Built:")
    print("  ✓ AI-powered SQL assistant using MCP")
    print("  ✓ Natural language to database queries")
    print("  ✓ Production-quality code")
    print("  ✓ Enterprise-ready architecture\n")
    
    print("Technologies Demonstrated:")
    print("  • Claude 3.5 Sonnet (AI reasoning)")
    print("  • Model Context Protocol (tool usage)")
    print("  • Python (backend)")
    print("  • Streamlit (UI)")
    print("  • SQLite (database)\n")
    
    print("Key Achievements:")
    print("  • Zero hardcoded schemas")
    print("  • Dynamic schema discovery")
    print("  • Business-friendly explanations")
    print("  • Safe, read-only queries")
    print("  • Clean, maintainable code\n")
    
    print("Ready to Run:")
    print("  → streamlit run app.py")
    print("  → python agent.py (command-line demo)\n")
    
    print("="*70)
    print("  Thank you for the demonstration!")
    print("="*70 + "\n")


def main():
    """Run the complete demo script."""
    try:
        demo_introduction()
        demo_architecture()
        demo_database()
        demo_example_queries()
        demo_ai_workflow()
        demo_security()
        demo_code_quality()
        demo_mcp_benefits()
        demo_use_cases()
        demo_extensions()
        demo_conclusion()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Demo error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Check if database exists
    if not os.path.exists('db.sqlite'):
        print("⚠️  Database not found. Running initialization...")
        os.system('python init_db.py')
        print()
    
    main()
