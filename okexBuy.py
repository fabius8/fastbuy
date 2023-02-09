import ccxt
import json
import sys
import requests
import time
from datetime import datetime, timedelta

print("例子: python okexBuy.py BLUR \"2023-02-14 20:00:00\" 1 100\n\n")

# 修改开始
coin = "BTC"
opentime = "2023-02-14 20:00:00"
buy_price = 1
buy_amount = 100
# 修改结束

if len(sys.argv) != 5:
    print("输入参数不对, python okexBuy.py <币对(BTC)-> <交易USD数量(如500)> <开盘时间\"2023-01-01 00:00:00\"> <价格> <数量>")
    sys.exit()
else:
    coin = sys.argv[1]
    opentime = sys.argv[2]
    opentime = opentime + ".000000"
    buy_price = float(sys.argv[3])
    buy_amount = float(sys.argv[4])

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
        "tdMode": "cash",
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
        timeB = datetime.strptime(opentime, "%Y-%m-%d %H:%M:%S.%f")
        timeA = datetime.now()
        if timeA > timeB:
            try:
                res = okexTrade(coin, okex, buy_price, buy_amount)
                print("交易完成!", res)
            except Exception as e:
                print("抢购失败!", type(e).__name__, str(e))
                pass
            timeC = datetime.now()
            print("交易耗时", (timeC - timeA).microseconds, "微秒")
            break
        else:
            print("距离", timeB, "剩余时间:", (timeB - timeA), end = '\r')
        time.sleep(0.05)