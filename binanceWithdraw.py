import ccxt
import json
import sys
import requests
import time
from datetime import datetime

# 修改区
coin = "MATIC"
amount = 10
network = "MATIC"
address = ""


config = json.load(open('config.json'))
exchange = {}

with open('addresses.txt', 'r') as f:
    addresses = [line.rstrip() for line in f]
print(addresses)

def exchangeInit(config):
    global exchange
    exchange["spot"] = ccxt.binance(config["binance"])
    exchange["spot"].load_markets()

def checkNetwork():
    res = exchange["spot"].sapi_get_capital_config_getall()
    for i in res:
        if i["coin"] == coin:
            for j in i["networkList"]:
                if j["network"] == network:
                    print(j)
    for i in res:
        if i["coin"] == coin:
            for j in i["networkList"]:
                if j["network"] == network:
                    #print(j)
                    return True
    return False

def exchangeWithdraw(coin, exchange, amount, address, network):
    res = exchange["spot"].withdraw(coin, amount, address, {"network": network})
    return res


if __name__ == '__main__':
    exchangeInit(config)
    if(checkNetwork() == False):
        print("network wrong!")
        exit(1)
    for addr in addresses:
        res = exchangeWithdraw(coin, exchange, amount, addr, network)
        print(res)
