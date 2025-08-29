"""
Setup script for EcoTracker AI with GEMINI integration.
This script helps users set up the environment and test the installation.
"""

import os
import shutil
import sys
from pathlib import Path

def setup_environment():
    """Setup the environment for EcoTracker AI."""
    print("🌱 Welcome to EcoTracker AI Setup!")
    print("=" * 40)
    
    # Check if .env exists
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from .env.example...")
        shutil.copy('.env.example', '.env')
        print("✅ .env file created!")
        print("⚠️  IMPORTANT: Please edit .env and add your GOOGLE_API_KEY")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  No .env.example found. Creating basic .env file...")
        with open('.env', 'w') as f:
            f.write("# EcoTracker AI Environment Variables\n")
            f.write("GOOGLE_API_KEY=your_google_api_key_here\n")
            f.write("FLASK_ENV=development\n")
            f.write("SECRET_KEY=dev-secret-change-me\n")
            f.write("DATABASE_URL=sqlite:///instance/ecotrack.db\n")
    
    # Check if instance directory exists
    instance_dir = Path('instance')
    if not instance_dir.exists():
        print("📁 Creating instance directory...")
        instance_dir.mkdir()
        print("✅ Instance directory created!")
    
    print("\n🚀 Setup complete! Next steps:")
    print("1. Edit .env file and add your GOOGLE_API_KEY")
    print("2. Run: python test_ai.py (to test AI integration)")
    print("3. Run: python seed.py (optional - for demo data)")
    print("4. Run: python app.py (to start the application)")

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'flask',
        'langchain',
        'google.generativeai',
        'dotenv'  # Changed from 'python-dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                # Special case for python-dotenv
                import dotenv
            else:
                __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed!")
        return True

if __name__ == "__main__":
    print("🔍 Checking dependencies...")
    deps_ok = check_dependencies()
    
    if deps_ok:
        print("\n🛠️  Setting up environment...")
        setup_environment()
    else:
        print("\n🛑 Please install dependencies first!")
        sys.exit(1)
