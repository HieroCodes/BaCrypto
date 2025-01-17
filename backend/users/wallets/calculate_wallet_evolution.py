from ..services import get_etherscan_transactions, get_crypto_prices
from datetime import datetime
from decimal import Decimal

def calculate_wallet_evolution(address, devise):
    # Récupérer les transactions et les prix
    transactions = get_etherscan_transactions(address)
    crypto_prices = get_crypto_prices(devise)
    
    # Vérifier que les transactions sont valides
    if transactions["status"] != "1" or not transactions["result"]:
        return {"error": "No transactions found for this address."}
    
    # Vérifier que le prix de l'ETH est disponible
    if "EUR" not in crypto_prices:
        return {"error": f"Failed to get price for {devise} in EUR."}
    
    eth_price_in_eur = Decimal(crypto_prices["EUR"])

    results = []
    for tx in transactions["result"]:
        # Récupérer la valeur de la transaction en Wei et la convertir en ETH
        tx_value_in_eth = Decimal(tx["value"]) / Decimal(10**18)  # Conversion de Wei à ETH
        
        # Calculer la valeur de la transaction en EUR
        tx_value_in_eur = tx_value_in_eth * eth_price_in_eur
        
        # Convertir le timestamp Unix en une date/heure lisible
        timestamp = int(tx["timeStamp"])
        date_time_utc = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
        date_time = date_time_utc.strftime('%Y-%m-%d %H:%M:%S')  # Format final en chaîne lisible
        
        # Ajouter le résultat à la liste
        results.append({
            "hash": tx["hash"],
            "value_in_ether": float(tx_value_in_eth),  # Valeur en ETH
            "value_in_eur": float(tx_value_in_eur),  # Valeur en EUR
            "date_time": date_time  # Date et heure de la transaction
        })
    
    return results

