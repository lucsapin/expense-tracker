#!/usr/bin/env python3
"""
Setup script for Enhanced Expense Tracker
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_virtual_environment():
    """Create and activate virtual environment."""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    return run_command(
        f"{sys.executable} -m venv .venv",
        "Creating virtual environment"
    )

def install_dependencies():
    """Install required packages."""
    # Determine the pip command based on OS
    if sys.platform.startswith('win'):
        pip_cmd = ".venv\\Scripts\\pip"
    else:
        pip_cmd = ".venv/bin/pip"
    
    return run_command(
        f"{pip_cmd} install -r requirements.txt",
        "Installing dependencies"
    )

def create_directories():
    """Create necessary directories."""
    directories = [
        "Expenses",
        "History", 
        "Summary",
        "charts"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    print("🚀 SETTING UP ENHANCED EXPENSE TRACKER")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not setup_virtual_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create directories
    create_directories()
    
    print("\n🎉 SETUP COMPLETE!")
    print("="*50)
    print("To start using the expense tracker:")
    print()
    print("1. Activate the virtual environment:")
    if sys.platform.startswith('win'):
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print()
    print("2. Run the main application:")
    print("   python run.py")
    print()
    print("3. Or run individual tools:")
    print("   python src/expense_tracker.py")
    print("   python src/budget_tracker.py")
    print("   python src/data_analyzer.py")
    print()
    print("📖 For more information, see README.md")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1) 