import ccxt
import json
import sys
import requests
import time
from datetime import datetime


config = json.load(open('config.json'))
exchange = {}

with open('addresses.txt', 'r') as f:
    addresses = [line.rstrip() for line in f]
print(addresses)

def exchangeInit(config):
    global exchange
    exchange["spot"] = ccxt.binance(config["binance"])
    exchange["spot"].load_markets()

def printSupportedNetworks(coin):
    res = exchange["spot"].sapi_get_capital_config_getall()
    for i in res:
        if i["coin"] == coin:
            print(f"\n{coin} supports the following networks:")
            for j in i["networkList"]:
                print("  -", j["network"])

def checkNetwork():
    res = exchange["spot"].sapi_get_capital_config_getall()
    for i in res:
        if i["coin"] == coin:
            for j in i["networkList"]:
                print(coin, "support network:", j["network"])
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

    # User input for coin, amount, and network
    coin = input("Enter the coin you want to withdraw: ")
    amount = float(input("Enter the amount you want to withdraw: "))
    printSupportedNetworks(coin) # Print supported networks for the coin
    network = input("Enter the network you want to use: ")


    if(checkNetwork() == False):
        print("network wrong!")
        exit(1)
    time.sleep(3)
    for addr in addresses:
        res = exchangeWithdraw(coin, exchange, amount, addr, network)
        print(addr, coin, amount, res)
        time.sleep(1)
