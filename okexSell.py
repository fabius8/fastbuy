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
sell_price = float(input("请输入卖出价格: "))
sell_amount = float(input("请输入卖出数量: "))

print("\nOKEX 抢开盘...")
print("卖出:", coin)
print("价格:", sell_price)
print("数量:", sell_amount)
print("交易金额(USDT):", sell_price*sell_amount)
print("提前多少时间卖出(毫秒):", diff)

config = json.load(open('config.json'))
exchange = {}

def exchangeInit(config):
    global exchange
    exchange["spot"] = ccxt.okx(config["okex"])
    exchange["spot"].load_markets()

def exchangeTrade(coin, exchange, sell_price, sell_amount):
    pair = coin + "-USDT"
    request = {
        "instId": pair,
        "tdMode": tdMode,
        "side": "sell",
        "ordType": "limit",
        "px": sell_price,
        "sz": sell_amount
    }
    res = exchange["spot"].private_post_trade_order(request)
    return res


if __name__ == '__main__':
    exchangeInit(config)
    while True:
        if "." in opentime:
            fmt = "%Y-%m-%d %H:%M:%S.%f"
        else:
            fmt = "%Y-%m-%d %H:%M:%S"
        timeB = datetime.strptime(opentime, fmt)
        timeA = datetime.now()
        if timeA + timedelta(microseconds=diff*1000) > timeB:
            try:
                res = exchangeTrade(coin, exchange, sell_price, sell_amount)
                print("交易完成!", res)
            except Exception as e:
                print("交易失败!", type(e).__name__, str(e))
                pass
            timeC = datetime.now()
            print("交易耗时", (timeC - timeA).microseconds/1000, "毫秒")
            break
        else:
            print("距离", timeB, "剩余时间:", (timeB - timeA), end = '\r')
        time.sleep(0)