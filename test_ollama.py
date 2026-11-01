"""
Quick test of Ollama integration
Tests that the agent can use local Llama model to query the database.
"""

import os
from agent import SQLAgent

# Make sure we don't use API key
if 'ANTHROPIC_API_KEY' in os.environ:
    del os.environ['ANTHROPIC_API_KEY']

print("="*60)
print("  Testing AI SQL Assistant with Local Llama (Ollama)")
print("="*60)
print()

# Initialize agent with Ollama
print("Initializing agent with Ollama...")
agent = SQLAgent(use_ollama=True, ollama_model="llama2:latest")
print()

# Test query
question = "Show top 5 customers by total revenue"
print(f"Question: {question}")
print()
print("Processing... (this may take 30-60 seconds with Llama)")
print()

try:
    response = agent.process_question(question)
    
    print("="*60)
    print("RESULTS")
    print("="*60)
    print()
    
    if response['sql']:
        print("Generated SQL:")
        print(response['sql'])
        print()
    
    if response['results']:
        print("Query Results:")
        print(f"Columns: {response['results'].get('columns', [])}")
        print(f"Rows: {response['results'].get('row_count', 0)}")
        if response['results'].get('rows'):
            print("\nTop 5:")
            for row in response['results']['rows'][:5]:
                print(f"  {row}")
        print()
    
    if response['explanation']:
        print("Business Explanation:")
        print(response['explanation'])
        print()
    
    print("="*60)
    print("✓ Test completed successfully!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
