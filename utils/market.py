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

        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",  # top by market cap
            "per_page": 10,              # top 10
            "page": 1,
            "sparkline": False
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
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

        return {}

    # def get_crypto_prices():
    #     cache_key = 'market:crypto_prices'
    #     prices = cache.get(cache_key)
    #     if prices:
    #         return prices

    #     url = "https://api.coingecko.com/api/v3/coins/markets"
    #     params = {
    #         "vs_currency": "usd",
    #         "ids": "bitcoin,ethereum",
    #         "order": "market_cap_desc",
    #         "per_page": 2,
    #         "page": 1,
    #         "sparkline": False
    #     }

    #     response = requests.get(url, params=params)

    #     if response.status_code == 200:
    #         data = response.json()
    #         formatted = {
    #             coin['id']: {
    #                 "symbol": coin['symbol'],
    #                 "name": coin['name'],
    #                 "price": coin['current_price'],
    #                 "market_cap": coin['market_cap'],
    #                 "volume_24h": coin['total_volume'],
    #                 "change_24h": coin['price_change_percentage_24h']
    #             }
    #             for coin in data
    #         }
    #         cache.set(cache_key, formatted, timeout=MarketService.CACHE_TIMEOUT)
    #         return formatted

    #     return {}


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
        symbols = symbols or ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA',]
                                # 'NVDA', 'META', 'NFLX', 'INTC', 'IBM',
                                # 'AMD', 'BA', 'BABA', 'PYPL', 'ORCL']
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
                quote = data.get("Global Quote", {})
                try:
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
                except (ValueError, TypeError):
                    continue


        # Cache the result
        cache.set(cache_key, results, timeout=MarketService.CACHE_TIMEOUT)
        return results
