import pandas as pd
import asyncio
from Exchange import Exchange
from Fetcher import fetch
from itertools import permutations
import datetime


async def main():
    print("Starting...")

    timestamp = datetime.datetime.now()
    bot = Exchange(initial_balance=10000)

    targets = ['binance', 'kucoin', 'bybit']
    symbol = "BTC/USDT"

    bot.trade_logs.append({
        "Time": timestamp,
        "Action": "NA",
        "Exchange": "NA",
        "Price": 0,
        "Amount": 0,
        "Status": "STARTED",
        "Balance_USDT": 10000,
        "Balance_BTC": 0,
    })

    bot.save_logs()

    while True:
        try:
            #Fetching the prices
            market_data = await fetch(targets, symbol)

            if market_data:
                best_opp = None
                highest_profit = -999

                #Creating the permutations
                for buy_ex, sell_ex in permutations(market_data, 2):

                    buy_price = float(buy_ex['Ask'])
                    sell_price = float(sell_ex['Bid'])

                    spread = sell_price - buy_price
                    spread_pct = (spread / buy_price) * 100

                    if highest_profit < spread_pct:
                        highest_profit = spread_pct
                        best_opp = {
                            "buy_exchange": buy_ex['Exchange'],
                            "sell_exchange": sell_ex['Exchange'],
                            "buy_price": buy_price,
                            "sell_price": sell_price,
                            "spread_pct": spread_pct,
                        }
                if best_opp:
                    #if best_opp['spread_pct'] > -0.2:
                        #print(f"The best opportunity: BUY {best_opp['buy_exchange']} --> SELL {best_opp['sell_exchange']} || SPREAD {best_opp['spread_pct']:.4f}")

                    if best_opp['spread_pct'] > 0.2:
                        print("Executing Trade")

                        bot.execute_trade("BUY", best_opp['buy_exchange'], best_opp['buy_price'], 0.01)
                        bot.execute_trade("SELL", best_opp['sell_exchange'], best_opp['sell_price'], 0.01)

                        bot.save_logs()
            #print("Runnning next cycle")
            await asyncio.sleep(5)

        except Exception as e:
            print(f"Global Error: {e}")
            await asyncio.sleep(5)

        finally:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot Stopped by User")
