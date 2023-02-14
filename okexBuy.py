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
diff = input("请输入提前几毫秒发送报文(默认0):")
if diff == "":
    diff = 0
else:
    diff = int(diff)
buy_price = float(input("请输入买入价格: "))
buy_amount = float(input("请输入买入数量: "))

print("\nOKEX 抢开盘...")
print("买入:", coin)
print("价格:", buy_price)
print("数量:", buy_amount)
print("交易金额(USDT):", buy_price*buy_amount)
print("提前多少时间买入(毫秒):", diff)

config = json.load(open('config.json'))
exchange = {}

def exchangeInit(config):
    global exchange
    exchange["spot"] = ccxt.okx(config["okex"])
    exchange["spot"].load_markets()

def exchangeTrade(coin, exchange, buy_price, buy_amount):
    pair = coin + "-USDT"
    request = {
        "instId": pair,
        "tdMode": tdMode,
        "side": "buy",
        "ordType": "limit",
        "px": buy_price,
        "sz": buy_amount
    }
    res = exchange["spot"].private_post_trade_order(request)
    return res


if __name__ == '__main__':
    exchangeInit(config)
    while True:
        timeB = datetime.strptime(opentime, "%Y-%m-%d %H:%M:%S")
        timeA = datetime.now()
        if timeA + timedelta(microseconds=diff*1000) > timeB:
            try:
                res = exchangeTrade(coin, exchange, buy_price, buy_amount)
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