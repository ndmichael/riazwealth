import requests
from django.core.cache import cache
from django.conf import settings


class MarketService:
    CACHE_TIMEOUT = 30  # seconds

    @staticmethod
    def get_crypto_prices():
        cache_key = 'market:crypto_prices'
        prices = cache.get(cache_key)
        if prices:
            return prices

        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, timeout=MarketService.CACHE_TIMEOUT)
            return data

        return {}

    @staticmethod
    def get_stock_prices(symbols=None):
        """
        Fetch stock prices using Alpha Vantage (or any stock API).
        """
        cache_key = 'market:stock_prices'
        prices = cache.get(cache_key)
        if prices:
            return prices

        # Set default symbols if none provided
        symbols = symbols or ['AAPL', 'GOOGL', 'MSFT']
        api_key = settings.ALPHA_VANTAGE_API_KEY  # Add this to your .env or settings

        url = "https://www.alphavantage.co/query"
        results = {}

        for symbol in symbols:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": api_key
            }
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                try:
                    price = float(data["Global Quote"]["05. price"])
                    results[symbol] = {"usd": price}
                except (KeyError, ValueError):
                    continue

        # Cache the result
        cache.set(cache_key, results, timeout=MarketService.CACHE_TIMEOUT)
        return results
