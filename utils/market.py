import requests
from django.core.cache import cache
from django.conf import settings


class MarketService:
    CACHE_TIMEOUT = 86400  # 1 day in seconds

    @staticmethod
    def get_crypto_prices():
        cache_key = 'market:crypto_prices'
        prices = cache.get(cache_key)
        if prices:
            return prices

        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": False
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            formatted = {
                coin['id']: {
                    "symbol": coin['symbol'],
                    "name": coin['name'],
                    "price": coin['current_price'],
                    "market_cap": coin['market_cap'],
                    "volume_24h": coin['total_volume'],
                    "change_24h": coin['price_change_percentage_24h']
                }
                for coin in data
            }
            cache.set(cache_key, formatted, timeout=MarketService.CACHE_TIMEOUT)
            return formatted

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Crypto API error: {e}")
            return prices or {}  # fallback to old cache or empty

    @staticmethod
    def get_stock_prices(symbols=None):
        cache_key = 'market:stock_prices'
        prices = cache.get(cache_key)
        if prices:
            return prices

        symbols = symbols or ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        # symbols = symbols or ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA',
        # 'NVDA', 'META', 'NFLX', 'INTC', 'IBM',
        # 'AMD', 'BA', 'BABA', 'PYPL', 'ORCL']
        api_key = settings.ALPHA_VANTAGE_API_KEY
        url = "https://www.alphavantage.co/query"
        results = {}

        try:
            for symbol in symbols[:5]:
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": api_key
                }
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                quote = data.get("Global Quote", {})
                results[symbol] = {
                    "symbol": quote.get("01. symbol"),
                    "open": float(quote.get("02. open", 0)),
                    "high": float(quote.get("03. high", 0)),
                    "low": float(quote.get("04. low", 0)),
                    "price": float(quote.get("05. price", 0)),
                    "volume": int(quote.get("06. volume", 0)),
                    "latest_trading_day": quote.get("07. latest trading day"),
                    "previous_close": float(quote.get("08. previous close", 0)),
                    "change": float(quote.get("09. change", 0)),
                    "change_percent": quote.get("10. change percent")
                }
            cache.set(cache_key, results, timeout=MarketService.CACHE_TIMEOUT)
            return results

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Stock API error: {e}")
            return prices or {}  # fallback
