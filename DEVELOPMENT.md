# Development Setup Guide

## Initial Setup

### 1. Python Environment (manual setup)
```powershell
# Windows (PowerShell)
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
Copy-Item .env.example .env
# Edit .env with your configuration
```

```bash
# Linux/macOS (bash)
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
# Edit .env with your configuration
```

### 3. (No Database)
This project uses in-memory order tracking. No database setup is required.

### 4. Configuration

Copy and edit `.env`:
```bash
cp .env.example .env
```

**Required Changes:**
- `BASE_URL`: Your target store URL
- `AFFILIATE_LINKS`: Comma-separated affiliate URLs
- `COUPON_CODES`: Comma-separated coupon codes
- `SELECTOR_*`: CSS selectors for your specific store

### 5. Run
```bash
# Validate configuration without executing
python -m src.main --dry-run

# Run simulation (default bots from .env)
python -m src.main --bots 5
```

## Development Workflow

### Running Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_order.py

# With coverage
pytest --cov=src --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

### Code Quality
```bash
# Format code
black src/ tests/
isort src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/
```

### Debugging

**Enable Visual Debugging:**
```env
HEADLESS=false
SLOW_MO=1000
LOG_LEVEL=DEBUG
```

**Check Specific Selectors:**
```python
# Create a test script
from playwright.async_api import async_playwright
import asyncio

async def test_selectors():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("YOUR_STORE_URL")
        
        # Test selector
        element = await page.query_selector("YOUR_SELECTOR")
        if element:
            print("Selector found!")
        else:
            print("Selector NOT found")
        
        await browser.close()

asyncio.run(test_selectors())
```

## Common Issues

### Playwright Installation Fails
```bash
# Try with sudo (Linux/Mac)
sudo playwright install chromium

# Windows: Run PowerShell as Administrator
```

### Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Selector Issues
1. Open browser in non-headless mode
2. Use browser DevTools to find correct selectors
3. Update `.env` with correct selectors
4. Test with `--dry-run` first

## IDE Setup

### VS Code
Recommended extensions:
- Python (Microsoft)
- Pylance
- Python Test Explorer
- Black Formatter
- GitLens

Settings (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true
}
```

### PyCharm
1. Set Python interpreter to venv
2. Enable pytest as test runner
3. Configure Black as external tool
4. Enable type checking

## Performance Tuning

### Optimize Concurrent Execution
```env
# Increase for more concurrency (resource-dependent)
MAX_CONCURRENT_BOTS=10

# Reduce delays for faster execution (less realistic)
ACTION_DELAY_MEAN=0.5
ACTION_DELAY_STD=0.2
```

### Performance Considerations
- Increase `MAX_CONCURRENT_BOTS` based on CPU/RAM capacity
- Reduce `ACTION_DELAY_*` for faster (less realistic) runs

## Production Deployment

### Environment Setup
```bash
# Use production .env
cp .env.example .env.production

# Set production values
HEADLESS=true
LOG_LEVEL=INFO
MAX_CONCURRENT_BOTS=20
```

### Running as Service (Linux)
```ini
# /etc/systemd/system/affiliate-bot.service
[Unit]
Description=Affiliate Bot QA Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/affiliate-bot-qa
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python -m src.main --bots 10
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Monitoring
```bash
# Log monitoring
tail -f logs/bot_execution.log

# Application monitoring only (no database)
```
