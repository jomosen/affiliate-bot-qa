"""Customer data generation service using Faker."""
from faker import Faker

from src.domain.models.order import CustomerInfo


class CustomerDataGenerator:
    """Service to generate realistic fake customer data."""

    def __init__(self, locale: str = "es_ES"):
        """Initialize with locale for region-specific data."""
        self.faker = Faker(locale)

    def generate_customer_info(self) -> CustomerInfo:
        """Generate complete customer information."""
        return CustomerInfo(
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            email=self.faker.email(),
            phone=self.faker.phone_number(),
            address=self.faker.street_address(),
            city=self.faker.city(),
            postcode=self.faker.postcode(),
        )
