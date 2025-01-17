from ..services import get_etherscan_transactions
from datetime import datetime

def calculate_wallet_evolution(address):
    transactions = get_etherscan_transactions(address)
    evolution = {}
    balance = 0

    for tx in transactions:
        date = datetime.fromtimestamp(int(tx["timeStamp"])).date()
        value = float(tx["value"]) / 10**18 

        if tx["to"] == address:
            balance += value
        elif tx["from"] == address:
            gas_fee = float(tx["gasUsed"]) * float(tx["gasPrice"]) / 10**18
            balance -= value + gas_fee

        evolution[date] = balance

    return [{"date": str(date), "price": price} for date, price in sorted(evolution.items())]
