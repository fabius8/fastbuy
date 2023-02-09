import ccxt
import json
import sys
import requests
import time
from datetime import datetime, timedelta

print("isolated: 逐仓\ncross: 全仓非保证金模式\ncash: 非保证金模式\n")
tdMode = input("请输入账户交易模式: ")

coin = input("请输入交易币种(如 BLUR ): ")
opentime = input("请输入开盘时间(2023-02-14 20:00:00): ")
buy_price = float(input("请输入买入价格: "))
buy_amount = float(input("请输入买入数量: "))

print("OKEX 抢开盘...")
print("买入:", coin)
print("价格:", buy_price)
print("数量:", buy_amount)
print("交易金额(USDT):", buy_price*buy_amount)

config = json.load(open('config.json'))
okex = {}

def okexInit(config):
    global okex
    okex["spot"] = ccxt.okx(config["okex"])
    okex["spot"].load_markets()

def okexTrade(coin, okex, buy_price, buy_amount):
    #okex["spot"].load_markets()
    pair = coin + "-USDT"
    request = {
        "instId": pair,
        "tdMode": tdMode,
        "side": "buy",
        "ordType": "limit",
        "px": buy_price,
        "sz": buy_amount
    }
    okex["spot"].private_post_trade_order(request)
    return request


if __name__ == '__main__':
    okexInit(config)
    while True:
        timeB = datetime.strptime(opentime, "%Y-%m-%d %H:%M:%S")
        timeA = datetime.now()
        if timeA > timeB:
            try:
                res = okexTrade(coin, okex, buy_price, buy_amount)
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