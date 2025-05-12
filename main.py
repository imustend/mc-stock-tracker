import time
import datetime

import yfinance as yf
import subprocess


MAX_RETRIES = 10
TMUX_SESSION_NAME = "vanilla"

def mcExec(command):
    subprocess.run(["tmux", "send-keys", "-t", TMUX_SESSION_NAME, str(command), "Enter"])




if __name__ == '__main__':
    #your stocks you want to track in format of display_name: yahoo_finance_ticker
    stocks = {"SP500": "^GSPC", "DJ30": "^DJI", "BLK": "BLK", "NVDA": "NVDA", "AAPL": "AAPL", "INTC": "INTC", "AMD":"AMD", "GME":"GME", "CDR.WA": "CDR.WA", "DINO":"DNP.WA", "JSW.WA":"JSW.WA"}
    pos = len(stocks)

    mcExec("scoreboard objectives add Price dummy")

    for name in stocks:
        mcExec("scoreboard players set " + name + " Price " + str(pos))
        mcExec("team add " + name + "Team")
        mcExec("team join " + name + "Team " + name)
        pos = pos - 1

    mcExec("scoreboard objectives setdisplay sidebar Price")


    while True:
        for name in stocks:
            retries = MAX_RETRIES
            stock = None
            while retries > 0 and stock is None:
                stock = yf.Ticker(stocks[name])
                retries -= 1
                time.sleep(2)
            
            if stock is None:
                now = datetime.datetime.now()
                now.isoformat()
                print("couldn't get " + name + " at: " + now)
                continue
            
            price = round(stock.info['regularMarketPrice'])
            state = stock.info['marketState']
            diff = round(stock.info['regularMarketChangePercent'], 2)
            fmtDiff = str(price) + "(" + str(diff) + "%)"
            color = ""
            if diff == 0.:
                color = "white"
            elif diff < 0.:
                color = "red"
            elif diff > 0.:
                color = "green"

            if state != "REGULAR":
                color = "dark_gray"

            mcExec("team modify " + name + "Team suffix {\"text\": \": "+ fmtDiff +"\",\"color\":\"" + color + "\"}")

        time.sleep(20)



