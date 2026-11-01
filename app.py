"""
Streamlit UI for AI SQL Assistant
Clean, professional dashboard for business intelligence queries.

Design Philosophy:
- Minimal, enterprise-style interface
- Focus on clarity and usability
- No unnecessary visual elements
- Professional color scheme
"""

import streamlit as st
import pandas as pd
from agent import SQLAgent
import os


# Page configuration
st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Custom CSS for professional appearance
st.markdown("""
<style>
    /* Clean, minimal styling */
    .main {
        padding: 2rem;
    }
    
    /* Headers */
    h1 {
        color: #1f2937;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #374151;
        font-weight: 500;
        font-size: 1.25rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    
    /* Section containers */
    .stExpander {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Code blocks */
    code {
        background-color: #f3f4f6;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'response' not in st.session_state:
        st.session_state.response = None
    if 'use_ollama' not in st.session_state:
        # Auto-detect: use Ollama if no API key set
        st.session_state.use_ollama = not bool(os.getenv('ANTHROPIC_API_KEY'))
    if 'api_key_set' not in st.session_state:
        st.session_state.api_key_set = bool(os.getenv('ANTHROPIC_API_KEY'))


def render_header():
    """Render application header."""
    st.title("AI SQL Assistant (Powered by MCP)")
    
    # Show which AI backend is being used
    if st.session_state.get('use_ollama', False):
        st.info("🦙 Using Local Llama Model (Ollama) - No API key required!")
    else:
        st.info("🤖 Using Claude API")
    
    st.markdown(
        "Ask natural language questions about your business data. "
        "The AI will analyze your database, generate SQL, and explain insights."
    )


def render_api_key_input():
    """Render API key input if not set."""
    # Add model selection
    with st.expander("⚙️ AI Model Configuration", expanded=False):
        model_choice = st.radio(
            "Select AI Backend:",
            ["Local Llama (Ollama)", "Claude API"],
            index=0 if st.session_state.get('use_ollama', True) else 1
        )
        
        st.session_state.use_ollama = (model_choice == "Local Llama (Ollama)")
        
        if st.session_state.use_ollama:
            st.success("✓ Using local Llama model - Free, no API key needed!")
            st.markdown("""
            **Requirements:**
            1. Install Ollama: `pip install ollama`
            2. Make sure Ollama is running locally
            3. Pull a model: `ollama pull llama3.2`
            
            [Get Ollama](https://ollama.ai/)
            """)
        else:
            if not st.session_state.api_key_set:
                st.warning("Please set your Anthropic API key to use Claude.")
                
                api_key = st.text_input(
                    "Anthropic API Key",
                    type="password",
                    help="Get your API key from https://console.anthropic.com/"
                )
                
                if st.button("Set API Key"):
                    if api_key:
                        os.environ['ANTHROPIC_API_KEY'] = api_key
                        st.session_state.api_key_set = True
                        st.session_state.use_ollama = False
                        st.success("API key set successfully!")
                        st.rerun()
                    else:
                        st.error("Please enter a valid API key")
                
                return False
            else:
                st.success("✓ Claude API key configured")
    
    return True


def render_example_questions():
    """Render example questions sidebar."""
    with st.expander("💡 Example Questions", expanded=False):
        examples = [
            "Show top 5 customers by total revenue",
            "Which products sell the most and why?",
            "What is the monthly revenue trend?",
            "Which customers have declining purchases?",
            "What countries generate the most revenue?",
            "Show average order value by customer",
            "Which products have the highest profit margins?",
            "Analyze seasonal trends in orders"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{example}", use_container_width=True):
                st.session_state.question = example


def render_query_input():
    """Render the main query input section."""
    st.markdown("### Ask a Question")
    
    # Two-column layout for input and button
    col1, col2 = st.columns([5, 1])
    
    with col1:
        question = st.text_input(
            "Question",
            placeholder="e.g., Show top 5 customers by revenue",
            label_visibility="collapsed",
            key="question"
        )
    
    with col2:
        run_query = st.button("Run Query", type="primary", use_container_width=True)
    
    return question, run_query


def render_sql_section(sql: str):
    """Render the generated SQL section."""
    st.markdown("## Generated SQL")
    
    if sql:
        st.code(sql, language="sql")
    else:
        st.info("SQL query will appear here after running your question.")


def render_results_section(results: dict):
    """Render the query results section."""
    st.markdown("## Query Results")
    
    if results:
        if 'error' in results:
            st.error(f"Query error: {results['error']}")
        elif results.get('rows'):
            # Convert to pandas DataFrame for better display
            df = pd.DataFrame(
                results['rows'],
                columns=results.get('columns', [])
            )
            
            # Display metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Rows Returned", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            
            # Display table
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            
            # Option to download results
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Results (CSV)",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )
        else:
            st.info("No results found.")
    else:
        st.info("Query results will appear here after running your question.")


def render_explanation_section(explanation: str):
    """Render the business explanation section."""
    st.markdown("## Business Insights")
    
    if explanation:
        # Parse explanation into bullet points if it contains line breaks
        lines = explanation.strip().split('\n')
        
        if len(lines) > 1:
            for line in lines:
                if line.strip():
                    # Format as bullet if not already
                    if line.strip().startswith('-') or line.strip().startswith('•'):
                        st.markdown(line)
                    else:
                        st.markdown(f"• {line}")
        else:
            st.markdown(explanation)
    else:
        st.info("Business insights will appear here after running your question.")


def process_query(question: str):
    """Process the user's query using the AI agent."""
    
    # Initialize agent if needed
    if st.session_state.agent is None:
        try:
            # Use llama2 if available, otherwise llama3.2
            ollama_model = "llama2:latest"  # Change to your installed model
            st.session_state.agent = SQLAgent(
                use_ollama=st.session_state.get('use_ollama', True),
                ollama_model=ollama_model
            )
        except ValueError as e:
            st.error(f"Failed to initialize agent: {str(e)}")
            return
    
    # Show progress
    with st.spinner("Analyzing database and generating query..."):
        try:
            # Reset conversation for new question
            st.session_state.agent.reset_conversation()
            
            # Process question
            response = st.session_state.agent.process_question(question)
            
            # Store response
            st.session_state.response = response
            
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
            st.session_state.response = None


def main():
    """Main application entry point."""
    
    # Initialize
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Check API key
    if not render_api_key_input():
        return
    
    # Render example questions
    render_example_questions()
    
    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Query input
    question, run_query = render_query_input()
    
    # Process query if button clicked
    if run_query and question:
        process_query(question)
    
    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display results if available
    if st.session_state.response:
        response = st.session_state.response
        
        # Three-column layout for results
        render_sql_section(response.get('sql'))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        render_results_section(response.get('results'))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        render_explanation_section(response.get('explanation'))
    else:
        # Empty state
        st.markdown("---")
        st.info(
            "👆 Enter a business question above to get started. "
            "The AI will explore your database, write SQL, and provide insights."
        )


if __name__ == "__main__":
    main()
