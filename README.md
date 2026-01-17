# Affiliate Bot QA

**Automated E2E Testing Suite for Referral & Conversion Systems**

A comprehensive Python-based purchase simulation system using Playwright for browser automation. Validates end-to-end referral links and coupon codes in e-commerce stores through realistic user behavior simulation.

## 🎯 Features

- **Concurrent Bot Execution**: Run multiple purchase simulations simultaneously with configurable concurrency
- **Dual Entry Methods**: 
  - Path A: Affiliate link entry with tracking validation
  - Path B: Homepage entry with coupon code application
- **Human Simulation**: Realistic delays, typing patterns, and browsing behavior using Gaussian distribution
- **Clean Architecture**: SOLID principles with separation of Domain, Application, Infrastructure, and Presentation layers
- **Page Object Model**: Maintainable browser automation with reusable page components
- **Comprehensive Testing**: Unit and integration tests with pytest

## 🏗️ Architecture

```
src/
├── domain/              # Business entities and models
│   └── models/         # Order, BotConfig, Customer entities
├── application/        # Use cases and business logic
│   ├── use_cases/     # ExecutePurchaseSimulation
│   ├── services/      # HumanSimulation, CustomerDataGenerator
│   └── factories/     # BotConfigFactory (Factory Pattern)
├── infrastructure/    # External integrations
│   ├── config/       # Settings management (pydantic-settings)
│   └── web/          # Playwright automation with Page Object Model
│       └── pages/    # HomePage, ProductPage, CartPage, CheckoutPage
└── presentation/     # CLI and orchestration
    ├── cli.py        # Argument parsing and logging setup
    └── bot_orchestrator.py  # Concurrent bot execution
```

## 📋 Prerequisites

- Python 3.10+
- Chrome/Chromium browser (installed automatically by Playwright)

## 🚀 Quick Start

### Setup on Windows (PowerShell)

```powershell
# Ensure Python 3.10+ is installed
python --version

# From the project root, create and activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies and Playwright browsers
pip install -r requirements.txt
playwright install chromium

# Copy and configure .env
Copy-Item .env.example .env
# Edit .env with your store URL, affiliate links, coupon codes, and selectors

# Validate configuration
python -m src.main --dry-run

# Run the simulation (default bots from .env)
python -m src.main --bots 5
```

Optional helper script:

```powershell
pwsh scripts/setup.ps1
```

### Setup on Linux/macOS (bash)

```bash
# Ensure Python 3.10+ is installed
python3 --version

# From the project root, create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and Playwright browsers
pip install -r requirements.txt
playwright install chromium

# Copy and configure .env
cp .env.example .env
# Edit .env with your store URL, affiliate links, coupon codes, and selectors

# Validate configuration
python -m src.main --dry-run

# Run the simulation (default bots from .env)
python -m src.main --bots 5
```

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd affiliate-bot-qa

# Create and activate virtual environment
python -m venv .venv            # Windows: use PowerShell and Activate.ps1
source .venv/bin/activate       # Windows (PowerShell): .\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

**Key Configuration Variables**:

```env
# Store Configuration
BASE_URL=https://your-store.com
MAX_CONCURRENT_BOTS=5

# Entry Methods
AFFILIATE_LINKS=https://store.com/?ref=aff1,https://store.com/?ref=aff2
COUPON_CODES=WELCOME10,SAVE20

# CSS Selectors Hub (customize for your store)
SELECTOR_ADD_TO_CART_BUTTON=button.add-to-cart
SELECTOR_PROCEED_TO_CHECKOUT=a.checkout-button
SELECTOR_PLACE_ORDER_BUTTON=#place_order
# ... (see .env.example for all selectors)
```

### 3. Run Simulations

```bash
# Run with default settings (from .env)
python -m src.main

# Run specific number of bots
python -m src.main --bots 10

# Validate configuration without running
python -m src.main --dry-run
```

## 🎮 Usage Examples

### Basic Execution
```bash
python -m src.main --bots 5
```

### Development Mode (Non-headless with slower execution)
```env
# In .env
HEADLESS=false
SLOW_MO=500
```

### Testing Configuration
```bash
# Validate settings and selectors
python -m src.main --dry-run
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_order.py

# Run with verbose output
pytest -v
```

## 📐 Design Patterns

### Clean Architecture
- **Domain Layer**: Pure business models and entities
- **Application Layer**: Use cases orchestrating domain logic
- **Infrastructure Layer**: External integrations (Browser, Config)
- **Presentation Layer**: CLI and user interaction

### SOLID Principles
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Extensible through protocols and interfaces
- **Interface Segregation**: Focused protocols (IBrowserAutomation)
- **Dependency Inversion**: Depend on abstractions, not concretions

### Factory Pattern
`BotConfigFactory` creates bot configurations with different strategies:
- `create_random_bot()`: Random affiliate/coupon selection
- `create_affiliate_bot()`: Dedicated affiliate link bots
- `create_coupon_bot()`: Dedicated coupon code bots

### Page Object Model (POM)
Separates page interactions from test logic:
- `BasePage`: Common operations (click, fill, wait)
- `HomePage`, `ProductPage`, `CartPage`, `CheckoutPage`: Page-specific logic

## 🔧 Customization

### Adding New Page Objects

```python
# src/infrastructure/web/pages/my_page.py
from src.infrastructure.web.base_page import BasePage

class MyPage(BasePage):
    async def my_action(self) -> None:
        await self.click("#my-selector")
```

### Extending Bot Behavior

```python
# src/application/factories/bot_config_factory.py
def create_special_bot(self, bot_id: int) -> BotConfig:
    return BotConfig(
        bot_id=bot_id,
        entry_method="special",
        # ... custom configuration
    )
```

### Custom Selectors

All CSS selectors are centralized in `.env` for easy updates:

```env
SELECTOR_ADD_TO_CART_BUTTON=.custom-add-to-cart, button[data-action="add"]
```

## 🐛 Troubleshooting

### Browser Issues
```bash
# Reinstall Playwright browsers
playwright install --force chromium
```

### Selector Issues
Enable non-headless mode to debug selectors:
```env
HEADLESS=false
SLOW_MO=1000
```

### Logging
Check logs for detailed execution information:
```bash
tail -f logs/bot_execution.log
```

## 📝 Code Style

This project follows:
- **PEP 8**: Python code style guide
- **Black**: Code formatting (100 char line length)
- **isort**: Import sorting
- **mypy**: Static type checking

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type check
mypy src/
```

## 🤝 Contributing

1. Follow Clean Architecture principles
2. Add tests for new features
3. Update documentation
4. Run linters before committing

## 📄 License

See LICENSE file for details.

## 🔗 Dependencies

Key libraries:
- **playwright**: Browser automation
- **pydantic-settings**: Configuration management
- **faker**: Fake data generation
- **loguru**: Logging
- **pytest**: Testing framework

See `requirements.txt` for complete list.

## 📚 Documentation

- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common commands and patterns
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development setup guide
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - AI agent instructions

## 🎯 Execution Flow

1. **Bot Creation**: Factory pattern generates bot configurations (affiliate/coupon)
2. **Browser Initialization**: Playwright launches with human simulation settings
3. **Navigation**: Bots enter via affiliate link or homepage
4. **Shopping**: Random product selection with realistic browsing
5. **Cart Management**: Randomize quantities (1-4 units per product)
6. **Checkout**: Fill forms with Faker-generated data
7. **Payment**: Select Cash on Delivery
8. **Order Completion**: Extract and log order numbers
9. **Results**: Display execution summary with success/failure counts

## 💡 Tips

- Start with `--dry-run` to validate configuration
- Use `HEADLESS=false` during development to see browser actions
- Adjust `ACTION_DELAY_MEAN` to control simulation speed
- Monitor `logs/bot_execution.log` for detailed execution traces
- Test selectors on target site before running full simulations
