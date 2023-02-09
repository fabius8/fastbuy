import ccxt
import json
import sys
import requests
import time
from datetime import datetime

coin = input("请输入交易币种(如 BLUR ): ")
opentime = input("请输入开盘时间(2023-02-14 20:00:00): ")
buy_price = float(input("请输入买入价格: "))
buy_amount = float(input("请输入买入数量: "))

print("\nMexc 抢开盘...")
print("买入:", coin)
print("价格:", buy_price)
print("数量:", buy_amount)
print("交易金额(USDT):", buy_price*buy_amount)

config = json.load(open('config.json'))
mexc = {}

def exchangeInit(config):
    global mexc
    mexc["spot"] = ccxt.mexc(config["mexc"])
    mexc["spot"].load_markets()

def exchangeTrade(coin, mexc, buy_price, buy_amount):
    pair = coin + "_USDT"
    request = {
        'symbol': pair,
        'price': str(buy_price),
        'quantity': str(buy_amount),
        'order_type': 'LIMIT_ORDER',
        'trade_type': 'BID'
    }
    res = mexc["spot"].spotPrivatePostOrderPlace(request)
    return res


if __name__ == '__main__':
    exchangeInit(config)
    while True:
        timeB = datetime.strptime(opentime, "%Y-%m-%d %H:%M:%S")
        timeA = datetime.now()
        if timeA > timeB:
            try:
                res = exchangeTrade(coin, mexc, buy_price, buy_amount)
                print("交易完成!", res)
            except Exception as e:
                print("抢购失败!", type(e).__name__, str(e))
                pass
            timeC = datetime.now()
            print("交易耗时", (timeC - timeA).microseconds/1000, "毫秒")
            break
        else:
            print("距离", timeB, "剩余时间:", (timeB - timeA), end = '\r')
        time.sleep(0.05)