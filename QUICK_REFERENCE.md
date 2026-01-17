# Quick Reference Guide

## Common Commands

### Setup
```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
Copy-Item .env.example .env  # Edit with your config
python -m src.main --dry-run
```

```bash
# Linux/macOS (bash)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env  # Edit with your config
python -m src.main --dry-run
```

### Running Simulations
```bash
# Default (5 bots from .env)
python -m src.main

# Specific number
python -m src.main --bots 10

# Non-headless for debugging (set in .env)
# HEADLESS=false, SLOW_MO=500
```

### Testing
```bash
pytest                          # All tests
pytest -v                       # Verbose
pytest --cov=src               # With coverage
pytest tests/unit/test_order.py # Specific file
```

### Code Quality
```bash
black src/ tests/     # Format
isort src/ tests/     # Sort imports
flake8 src/ tests/    # Lint
mypy src/             # Type check
```

## Project Structure Quick Map

```
src/
├── domain/              # ⚙️ Business Logic (NO external dependencies)
│   ├── models/         # Order, BotConfig, CustomerInfo
│   └── models/         # Pure dataclasses (no persistence)
│
├── application/        # 🎯 Use Cases & Services
│   ├── use_cases/     # ExecutePurchaseSimulation
│   ├── services/      # HumanSimulation, CustomerDataGenerator
│   └── factories/     # BotConfigFactory
│
├── infrastructure/    # 🔌 External Integrations
│   ├── config/       # Settings (pydantic)
│   └── web/          # Playwright + Page Objects
│
└── presentation/     # 🖥️ CLI & Orchestration
    └── main.py       # Entry point
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `src/main.py` | Application entry point |
| `src/domain/models/order.py` | Core Order entity |
| `src/application/use_cases/execute_purchase_simulation.py` | Main use case |
| `src/infrastructure/web/playwright_automation.py` | Browser automation |
| `src/infrastructure/config/settings.py` | Configuration management |
| `src/presentation/bot_orchestrator.py` | Concurrent execution |
| `.env` | Configuration (copy from `.env.example`) |

## Configuration Essentials

### Must Configure in .env
```env
BASE_URL=https://your-store.com
AFFILIATE_LINKS=url1,url2,url3
COUPON_CODES=CODE1,CODE2
```

### Selectors to Customize
```env
SELECTOR_ADD_TO_CART_BUTTON=button.add-to-cart
SELECTOR_PROCEED_TO_CHECKOUT=.checkout-button
SELECTOR_PLACE_ORDER_BUTTON=#place_order
SELECTOR_PAYMENT_METHOD_COD=#payment_method_cod
SELECTOR_TERMS_CHECKBOX=#terms
```

## Architecture Rules (Clean Architecture)

### ✅ Allowed Dependencies
- Domain → Nothing (pure business logic)
- Application → Domain
- Infrastructure → Domain (implements interfaces)
- Presentation → Application + Infrastructure

### ❌ Forbidden Dependencies
- Domain → Infrastructure (NEVER)
- Domain → Application (NEVER)
- Application → Infrastructure (use interfaces)
- Infrastructure → Presentation (NEVER)

## Common Patterns

### Adding a New Page Object
```python
# src/infrastructure/web/pages/new_page.py
from src.infrastructure.web.base_page import BasePage

class NewPage(BasePage):
    def __init__(self, page, human_sim, settings):
        super().__init__(page, human_sim)
        self.settings = settings
    
    async def custom_action(self):
        await self.click(self.settings.selector_custom)
```

### Using Human Simulation
```python
await self.human_sim.delay_action()     # Between actions
await self.human_sim.delay_typing()     # Between keystrokes
qty = self.human_sim.random_quantity()  # Random 1-4
```

### Order Lifecycle (In-Memory)
```python
# Domain order object created and updated during simulation
# No persistence layer; results are summarized at the end
```

### Logging
```python
from loguru import logger

logger.info("Info message")
logger.success("Success message")
logger.error("Error message")
logger.exception("Error with traceback")
```

## Debugging Tips

### Enable Visual Mode
```env
HEADLESS=false
SLOW_MO=1000
```

### Check Selectors
```bash
# Run dry-run to validate config
python -m src.main --dry-run

# Test in non-headless with slow-mo
# Watch the browser to see where it fails
```

### Environment Checks
```bash
# Ensure venv is active and browsers installed
python -m src.main --dry-run
```

### View Logs
```bash
# Real-time
tail -f logs/bot_execution.log

# Search for errors
grep ERROR logs/bot_execution.log
```

## Testing Patterns

### Unit Test (Domain)
```python
def test_order_add_item():
    order = Order()
    item = OrderItem(...)
    order.add_item(item)
    assert order.subtotal == item.total_price
```

### Async Test
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

## Performance Tuning

### More Concurrency
```env
MAX_CONCURRENT_BOTS=20  # Increase (CPU/RAM dependent)
```

### Faster Execution (Less Realistic)
```env
ACTION_DELAY_MEAN=0.5   # Reduce delays
ACTION_DELAY_STD=0.1
TYPING_DELAY_MIN=10
TYPING_DELAY_MAX=30
```

### Slower (More Realistic)
```env
ACTION_DELAY_MEAN=3.0
ACTION_DELAY_STD=1.0
TYPING_DELAY_MIN=100
TYPING_DELAY_MAX=300
```

## Troubleshooting Checklist

- [ ] Virtual environment activated?
- [ ] Dependencies installed? (`pip install -r requirements.txt`)
- [ ] Playwright browsers installed? (`playwright install chromium`)
- [ ] `.env` file exists? (`cp .env.example .env`)
- [ ] Selectors correct for your store?
- [ ] Base URL accessible?

## Resources

- Playwright Docs: https://playwright.dev/python/
 
- Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
