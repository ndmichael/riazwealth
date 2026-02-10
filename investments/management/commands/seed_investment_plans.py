from django.core.management.base import BaseCommand
from investments.models import InvestmentPlan

class Command(BaseCommand):
    help = "Seed or update investment plans"

    def handle(self, *args, **options):
        plans = [
            {
                "name": "Stocks",
                "description": """Invest in a diversified portfolio of top-performing stocks across various industries.
Our stock investment plan aims to deliver a steady growth of 36% monthly.
Ideal for investors looking for moderate risk with the potential for significant returns through equity markets.""",
                "min_amount": 100,
                "max_amount": 5_000_000,
                "daily_profit_rate": 1.0,
                "image": "investment_plan_img/stocks.jpg",
            },
            {
                "name": "Trade Bonds",
                "description": """Secure your wealth with trade bonds that offer a fixed return of 45% monthly profit.
Designed for investors seeking stability and predictable income streams from bond markets.""",
                "min_amount": 200,
                "max_amount": 5_000_000,
                "daily_profit_rate": 1.2,
                "image": "investment_plan_img/bonds.jpg",
            },
            {
                "name": "Real Estate",
                "description": """Capitalize on the growth of the real estate market by investing in residential and commercial properties.
Offers stable income and long-term appreciation.""",
                "min_amount": 1000,
                "max_amount": 5_000_000,
                "daily_profit_rate": 2.0,
                "image": "investment_plan_img/realestate.jpg",
            },
            {
                "name": "Gold and Silver",
                "description": """Invest in precious metals like gold and silver to hedge against inflation
and preserve wealth with consistent returns.""",
                "min_amount": 500,
                "max_amount": 5_000_000,
                "daily_profit_rate": 1.5,
                "image": "investment_plan_img/precious_stones.jpg",
            },
            {
                "name": "Bitcoin and Cryptocurrencies",
                "description": """High-growth crypto investment plan for investors willing to accept higher risk
in exchange for potentially high returns.""",
                "min_amount": 100,
                "max_amount": 5_000_000,
                "daily_profit_rate": 1.0,
                "image": "investment_plan_img/bitcoin.jpg",
            },
            {
                "name": "Oil and Gas",
                "description": """Profit from the energy sector with balanced risk and stable returns
from oil and gas investments.""",
                "min_amount": 500,
                "max_amount": 5_000_000,
                "daily_profit_rate": 1.5,
                "image": "investment_plan_img/oil_gas.jpg",
            },
            {
                "name": "AI and Web3",
                "description": """Invest in AI and Web3 technologies for exposure to cutting-edge,
high-growth digital innovation.""",
                "min_amount": 1000,
                "max_amount": 5_000_000,
                "daily_profit_rate": 2.0,
                "image": "investment_plan_img/ai_web3.jpg",
            },
        ]

        for plan in plans:
            obj, created = InvestmentPlan.objects.update_or_create(
                name=plan["name"],
                defaults=plan,
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated {obj.name}"))