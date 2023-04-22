import ccxt
import json
import sys
import requests
import time
from datetime import datetime

coin = input("请输入交易币种(如 IRON ): ")
opentime = input("请输入开盘时间(2023-02-14 20:00:00): ")
sell_price = float(input("请输入卖出价格: "))
sell_amount = float(input("请输入卖出数量: "))

print("\nGate 开盘抢卖...")
print("卖出:", coin)
print("价格:", sell_price)
print("数量:", sell_amount)
print("交易金额(USDT):", sell_price*sell_amount)

config = json.load(open('config.json'))
exchange = {}

def exchangeInit(config):
    global exchange
    exchange["spot"] = ccxt.gate(config["gate"])
    exchange["spot"].load_markets()

def exchangeTrade(coin, exchange, sell_price, sell_amount):
    pair = coin + "/USDT"
    res = exchange["spot"].createLimitSellOrder(pair, sell_amount, sell_price)
    return res


if __name__ == '__main__':
    exchangeInit(config)
    while True:
        timeB = datetime.strptime(opentime, "%Y-%m-%d %H:%M:%S")
        timeA = datetime.now()
        if timeA > timeB:
            try:
                res = exchangeTrade(coin, exchange, sell_price, sell_amount)
                print("发送成功!", res)
            except Exception as e:
                print("交易失败!", type(e).__name__, str(e))
                pass
            timeC = datetime.now()
            print("交易耗时", (timeC - timeA).microseconds/1000, "毫秒")
            break
        else:
            print("距离", timeB, "剩余时间:", (timeB - timeA), end = '\r')
        time.sleep(0.05)