# AI Coding Agent Instructions

## Project Overview
This is a Python E2E testing suite for e-commerce referral and coupon validation using **Clean Architecture**, **Playwright** browser automation, and **in-memory order tracking**. The system simulates concurrent user purchases via affiliate links or coupon codes with realistic human behavior.

## Architecture (Critical Understanding)

### Layer Boundaries (NEVER violate these)
1. **Domain** (`src/domain/`) - Pure business logic, zero dependencies
   - Models: `Order`, `BotConfig`, `CustomerInfo`, `OrderItem`
   - No persistence interfaces - orders are tracked in memory
   - Changes here require careful consideration - this is the core

2. **Application** (`src/application/`) - Use cases and services
   - `ExecutePurchaseSimulation` - main use case orchestrating full purchase flow
   - `HumanSimulationService` - Gaussian delays and realistic behavior
   - `BotConfigFactory` - Factory Pattern for creating bot configurations

3. **Infrastructure** (`src/infrastructure/`) - External integrations
   - Web: Playwright automation with **Page Object Model**
   - Config: Pydantic Settings loading from `.env`

4. **Presentation** (`src/presentation/`) - CLI and orchestration
   - Entry point: `src/main.py`
   - `BotOrchestrator` - manages concurrent bot execution with semaphores

### Dependency Flow
**ALWAYS** flow inward: Presentation → Application → Domain  
Infrastructure implements protocols but never depends on Application/Presentation

## Critical Development Workflows

### Adding New Page Objects
```python
# 1. Create in src/infrastructure/web/pages/
# 2. Inherit from BasePage
# 3. Use self.human_sim for delays
# 4. Access settings via self.settings for selectors
class NewPage(BasePage):
    def __init__(self, page, human_sim, settings: Settings):
        super().__init__(page, human_sim)
        self.settings = settings
```

### Selector Management
**ALL** selectors live in `.env` under `SELECTOR_*` prefix. Never hardcode selectors in page objects.

```python
# ✅ Correct
await self.click(self.settings.selector_add_to_cart_button)

# ❌ Wrong
await self.click("button.add-to-cart")
```

### Running the Application
```bash
# Development
python -m src.main --bots 5

# Validate config
python -m src.main --dry-run
```

### Testing Requirements
- Unit tests for domain models (no external dependencies)
- Use `@pytest.mark.asyncio` for async tests
- Mock external dependencies in application layer tests
- Integration tests should focus on Playwright interactions

## Project-Specific Conventions

### Async/Await Everywhere
This is an **async-first** codebase. All I/O operations use `asyncio`:
- Playwright: `await page.click()`
- Use cases: `async def execute()`

### Logging with Loguru
```python
from loguru import logger

logger.info("Standard message")
logger.success("Completion message")
logger.error("Error with context")
logger.exception("Automatic traceback")
```

### Human Simulation Pattern
Always use `HumanSimulationService` for delays:
```python
await self.human_sim.delay_action()  # Between actions
await self.human_sim.delay_typing()  # Between keystrokes
```

### Configuration Loading
```python
from src.infrastructure.config.settings import get_settings

settings = get_settings()  # Cached singleton
affiliate_links = settings.get_affiliate_links_list()  # Helper methods
```

## Common Pitfalls

1. **Playwright Initialization**: Must call `await browser.initialize()` before use
2. **Type Hints**: Required on all function signatures (enforced by mypy)
3. **Bot IDs**: Passed through `BotConfig.bot_id`, used for logging context
4. **Order Tracking**: Orders exist only in memory during execution - no persistence layer

## File Organization Rules

- Models go in `domain/models/` (pure dataclasses with business logic)
- Page objects in `infrastructure/web/pages/`
- Services in `application/services/`
- Use cases in `application/use_cases/`

## Integration Points

### Entry Methods (Two Paths)
```python
# Path A: Affiliate Link
await browser.navigate(config.affiliate_link)

# Path B: Coupon Code  
await browser.navigate(base_url)
# ... later in checkout ...
await checkout_page.apply_coupon(config.coupon_code)
```

### Order Lifecycle
1. Create `Order` domain object
2. Populate via use case execution
3. `order.mark_completed(order_number)` or `order.mark_failed(error)`
4. Order returned to orchestrator for summary reporting

## Code Style Enforcement
- Black (100 char line length)
- isort (black profile)
- mypy (strict mode)
- PEP 8 naming conventions

When making changes, ensure domain logic stays in domain layer - resist the temptation to put business rules in infrastructure or presentation layers.
