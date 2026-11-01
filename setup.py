"""
Quick Setup Script
Automates project initialization and validation.
"""

import os
import subprocess
import sys


def print_header(message):
    """Print formatted header."""
    print("\n" + "="*60)
    print(f"  {message}")
    print("="*60 + "\n")


def check_python_version():
    """Verify Python version is 3.9+."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Error: Python 3.9+ required")
        sys.exit(1)
    
    print("✓ Python version is compatible")


def install_dependencies():
    """Install required packages."""
    print_header("Installing Dependencies")
    
    print("Installing packages from requirements.txt...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"
        ])
        print("✓ All dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        print("Try manually: pip install -r requirements.txt")
        sys.exit(1)


def initialize_database():
    """Create and seed the database."""
    print_header("Initializing Database")
    
    if os.path.exists("db.sqlite"):
        response = input("Database already exists. Recreate? (y/N): ")
        if response.lower() != 'y':
            print("⏭️  Skipping database initialization")
            return
    
    print("Creating database with seed data...")
    try:
        subprocess.check_call([sys.executable, "init_db.py"])
        print("✓ Database initialized successfully")
    except subprocess.CalledProcessError:
        print("❌ Error initializing database")
        sys.exit(1)


def check_env_file():
    """Check for environment configuration."""
    print_header("Checking Configuration")
    
    if os.path.exists(".env"):
        print("✓ .env file found")
        
        # Check if API key is set
        with open(".env", "r") as f:
            content = f.read()
            if "ANTHROPIC_API_KEY" in content and "your-api-key-here" not in content:
                print("✓ API key appears to be configured")
            else:
                print("⚠️  Warning: Please set your ANTHROPIC_API_KEY in .env file")
    else:
        print("⚠️  No .env file found")
        print("Creating .env from template...")
        
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as src:
                with open(".env", "w") as dst:
                    dst.write(src.read())
            print("✓ Created .env file")
            print("⚠️  Please edit .env and add your ANTHROPIC_API_KEY")
        else:
            print("❌ .env.example not found")
    
    # Check environment variable
    if os.getenv("ANTHROPIC_API_KEY"):
        print("✓ ANTHROPIC_API_KEY environment variable is set")
    else:
        print("⚠️  ANTHROPIC_API_KEY not set in environment")
        print("   You can set it in .env file or as an environment variable")


def print_next_steps():
    """Print instructions for running the application."""
    print_header("Setup Complete!")
    
    print("Next steps:")
    print()
    print("1. Set your Anthropic API key:")
    print("   - Edit .env file, OR")
    print("   - Set environment variable:")
    print("     Windows (PowerShell): $env:ANTHROPIC_API_KEY = 'your-key'")
    print("     Windows (CMD):        set ANTHROPIC_API_KEY=your-key")
    print("     Linux/Mac:            export ANTHROPIC_API_KEY=your-key")
    print()
    print("2. Run the Streamlit UI:")
    print("   streamlit run app.py")
    print()
    print("3. Or test the agent directly:")
    print("   python agent.py")
    print()
    print("📚 See README.md for detailed documentation")
    print()


def main():
    """Run the setup process."""
    print_header("AI SQL Assistant - Setup")
    
    # Run setup steps
    check_python_version()
    install_dependencies()
    initialize_database()
    check_env_file()
    
    # Show next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed: {str(e)}")
        sys.exit(1)
