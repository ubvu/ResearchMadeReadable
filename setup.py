
"""
Setup script for the Research Summary Application.
"""
import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages."""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        sys.exit(1)

def setup_database():
    """Set up the database."""
    try:
        print("Setting up database...")
        from src.database.models import create_tables
        create_tables()
        print("✅ Database setup completed!")
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)

def create_directories():
    """Create necessary directories."""
    directories = [
        "data/uploads",
        "data/exports",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function."""
    print("🔧 Setting up Research Summary Application...")
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Install requirements
    install_requirements()
    
    # Create directories
    create_directories()
    
    # Setup database
    setup_database()
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("streamlit run app.py")
    print("\nThe application will be available at http://localhost:8501")

if __name__ == "__main__":
    main()
