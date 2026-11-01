"""
System Validation Tests
Verifies that all components are properly set up and functional.

Run this before deploying or demonstrating the project.
"""

import os
import sys
import sqlite3
import json


def print_test(test_name, passed, message=""):
    """Print test result with formatting."""
    status = "✓" if passed else "❌"
    print(f"{status} {test_name}")
    if message:
        print(f"  → {message}")


def test_python_version():
    """Verify Python version is 3.9+."""
    version = sys.version_info
    passed = version.major >= 3 and version.minor >= 9
    print_test(
        "Python Version",
        passed,
        f"Python {version.major}.{version.minor}.{version.micro}"
    )
    return passed


def test_dependencies():
    """Check if required packages are installed."""
    required = ['anthropic', 'streamlit', 'pandas', 'mcp']
    all_installed = True
    
    for package in required:
        try:
            __import__(package)
            print_test(f"Package: {package}", True)
        except ImportError:
            print_test(f"Package: {package}", False, "Not installed")
            all_installed = False
    
    return all_installed


def test_database_exists():
    """Check if database file exists."""
    exists = os.path.exists('db.sqlite')
    print_test(
        "Database File",
        exists,
        "db.sqlite found" if exists else "Run: python init_db.py"
    )
    return exists


def test_database_schema():
    """Verify database has correct tables and data."""
    try:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['customers', 'products', 'orders']
        all_present = all(table in tables for table in required_tables)
        
        print_test(
            "Database Tables",
            all_present,
            f"Found: {', '.join(tables)}"
        )
        
        if not all_present:
            conn.close()
            return False
        
        # Check row counts
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        
        print_test(
            "Database Data",
            customer_count > 0 and product_count > 0 and order_count > 0,
            f"{customer_count} customers, {product_count} products, {order_count} orders"
        )
        
        conn.close()
        return True
        
    except Exception as e:
        print_test("Database Schema", False, str(e))
        return False


def test_database_relationships():
    """Verify foreign key relationships work."""
    try:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        
        # Test join query
        cursor.execute("""
            SELECT COUNT(*) 
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            JOIN products p ON o.product_id = p.id
        """)
        
        join_count = cursor.fetchone()[0]
        conn.close()
        
        passed = join_count > 0
        print_test(
            "Database Joins",
            passed,
            f"{join_count} joined records"
        )
        
        return passed
        
    except Exception as e:
        print_test("Database Joins", False, str(e))
        return False


def test_api_key_configured():
    """Check if Anthropic API key is set."""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if api_key:
        # Don't print the actual key
        masked = api_key[:7] + "..." if len(api_key) > 7 else "***"
        print_test(
            "API Key (Environment)",
            True,
            f"Set: {masked}"
        )
        return True
    
    # Check .env file
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            if 'ANTHROPIC_API_KEY' in content and 'your-api-key-here' not in content:
                print_test(
                    "API Key (.env file)",
                    True,
                    "Configured in .env"
                )
                return True
    
    print_test(
        "API Key",
        False,
        "Not configured. Set ANTHROPIC_API_KEY environment variable or edit .env"
    )
    return False


def test_file_structure():
    """Verify all required files exist."""
    required_files = [
        'app.py',
        'agent.py',
        'server.py',
        'init_db.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_present = True
    for file in required_files:
        exists = os.path.exists(file)
        if not exists:
            print_test(f"File: {file}", False, "Missing")
            all_present = False
    
    if all_present:
        print_test(
            "Project Files",
            True,
            "All required files present"
        )
    
    return all_present


def test_agent_initialization():
    """Test if agent can be initialized."""
    try:
        # Only test if API key is available
        if not os.getenv('ANTHROPIC_API_KEY'):
            print_test(
                "Agent Initialization",
                None,
                "Skipped (no API key)"
            )
            return None
        
        from agent import SQLAgent
        agent = SQLAgent()
        
        print_test(
            "Agent Initialization",
            True,
            "SQLAgent created successfully"
        )
        return True
        
    except Exception as e:
        print_test(
            "Agent Initialization",
            False,
            str(e)
        )
        return False


def test_sample_query():
    """Test a simple database query."""
    try:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        
        # Simple aggregation query
        cursor.execute("""
            SELECT 
                c.name,
                COUNT(o.id) as order_count
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id
            ORDER BY order_count DESC
            LIMIT 5
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        passed = len(results) > 0
        print_test(
            "Sample Query Execution",
            passed,
            f"Retrieved {len(results)} customers"
        )
        
        return passed
        
    except Exception as e:
        print_test(
            "Sample Query Execution",
            False,
            str(e)
        )
        return False


def run_all_tests():
    """Run comprehensive system validation."""
    print("\n" + "="*60)
    print("  AI SQL Assistant - System Validation")
    print("="*60 + "\n")
    
    print("📋 Running Tests...\n")
    
    results = {}
    
    # Core requirements
    print("Core Requirements:")
    results['python'] = test_python_version()
    results['files'] = test_file_structure()
    print()
    
    # Dependencies
    print("Dependencies:")
    results['packages'] = test_dependencies()
    print()
    
    # Database
    print("Database:")
    results['db_exists'] = test_database_exists()
    if results['db_exists']:
        results['db_schema'] = test_database_schema()
        results['db_joins'] = test_database_relationships()
        results['query'] = test_sample_query()
    print()
    
    # Configuration
    print("Configuration:")
    results['api_key'] = test_api_key_configured()
    print()
    
    # Agent
    print("Agent:")
    results['agent'] = test_agent_initialization()
    print()
    
    # Summary
    print("="*60)
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    total = len(results)
    
    print(f"\n✓ Passed: {passed}/{total}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{total}")
    if skipped > 0:
        print(f"⏭️  Skipped: {skipped}/{total}")
    
    print()
    
    # Recommendations
    if failed > 0:
        print("⚠️  Action Required:")
        if not results.get('packages'):
            print("  → Run: pip install -r requirements.txt")
        if not results.get('db_exists') or not results.get('db_schema'):
            print("  → Run: python init_db.py")
        if not results.get('api_key'):
            print("  → Set ANTHROPIC_API_KEY environment variable")
        print()
    
    # Next steps
    if failed == 0 and passed > 0:
        print("🎉 System Ready!")
        print("\nNext Steps:")
        print("  → Start the UI:  streamlit run app.py")
        print("  → Test the agent: python agent.py")
        print()
    
    return failed == 0


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite failed: {str(e)}")
        sys.exit(1)
