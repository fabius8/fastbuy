import ccxt
import json
import sys
import requests
import time
from datetime import datetime

# 修改区
coin = "USDT"
amount = 11
fee = 1
network = "USDT-TRC20"

config = json.load(open('config.json'))
exchange = {}

with open('addresses.txt', 'r') as f:
    addresses = [line.rstrip() for line in f]
print(addresses)
time.sleep(5)

def exchangeInit(config):
    global exchange
    exchange["spot"] = ccxt.okx(config["okex"])
    exchange["spot"].load_markets()


def exchangeWithdraw(coin, exchange, amount, address, network, fee):
    res = exchange["spot"].withdraw(coin, amount, address, {"chain": network, "fee": fee, "pwd": config["okex"]["pwd"]})
    return res


if __name__ == '__main__':
    exchangeInit(config)
    
    for addr in addresses:
        res = exchangeWithdraw(coin, exchange, amount, addr, network, fee)
        print(res)
        time.sleep(1)