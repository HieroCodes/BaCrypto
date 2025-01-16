import requests
from django.conf import settings

def get_etherscan_transactions(address):
    url = f"https://api.etherscan.io/api"
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': settings.ETHERSCAN_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def get_crypto_prices(symbol):
    url = f"https://min-api.cryptocompare.com/data/price"
    params = {
        'fsym': symbol,
        'tsyms': 'USD,EUR',
        'api_key': settings.CRYPTOCOMPARE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()