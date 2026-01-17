"""Setup script to quickly configure the project."""
import os
import sys
from pathlib import Path


def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✓ .env file already exists")
        return
    
    if not env_example.exists():
        print("✗ .env.example not found!")
        return
    
    env_file.write_text(env_example.read_text())
    print("✓ Created .env file from .env.example")
    print("⚠ Please edit .env with your store configuration")


def create_logs_directory():
    """Create logs directory if it doesn't exist."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("✓ Created logs/ directory")
    else:
        print("✓ logs/ directory exists")


def check_python_version():
    """Check if Python version is 3.10+."""
    if sys.version_info < (3, 10):
        print(f"✗ Python 3.10+ required (current: {sys.version_info.major}.{sys.version_info.minor})")
        return False
    print(f"✓ Python version: {sys.version_info.major}.{sys.version_info.minor}")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required = ["playwright", "sqlalchemy", "pydantic", "faker", "loguru"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} NOT installed")
    
    if missing:
        print("\n⚠ Install dependencies with: pip install -r requirements.txt")
        return False
    return True


def main():
    """Run setup checks and configuration."""
    print("=" * 60)
    print("Affiliate Bot QA - Setup Script")
    print("=" * 60)
    print()
    
    # Check Python version
    print("Checking Python version...")
    if not check_python_version():
        sys.exit(1)
    print()
    
    # Create necessary files/directories
    print("Creating configuration files...")
    create_env_file()
    create_logs_directory()
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    # Next steps
    print("=" * 60)
    print("Next Steps:")
    print("=" * 60)
    
    if not deps_ok:
        print("1. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("   playwright install chromium")
    
    print("2. Configure .env file with your store details:")
    print("   - BASE_URL")
    print("   - AFFILIATE_LINKS")
    print("   - COUPON_CODES")
    print("   - Database credentials")
    print("   - CSS selectors")
    
    print("\n3. Initialize database:")
    print("   python -m src.main --init-db")
    
    print("\n4. Test configuration:")
    print("   python -m src.main --dry-run")
    
    print("\n5. Run simulation:")
    print("   python -m src.main --bots 5")
    
    print("\n" + "=" * 60)
    print("For detailed documentation, see README.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
