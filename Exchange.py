import pandas as pd
import datetime

class Exchange:
    def __init__(self, initial_balance):
        self.balance = {"USDT": initial_balance, "BTC": 0}
        self.trade_logs  = []
        self.fees = 0.001 #As Fees is normally 0.1%

    def save_logs(self):
        #Saving the trading logs to a dataframe
        df = pd.DataFrame(self.trade_logs)
        df.to_csv("trade_logs.csv", index=False)
        return df

    def get_balance(self):
        return self.balance

    def execute_trade(self, action, exchange_name, price, amount):
        status = "Failed"
        timestamp = datetime.datetime.now()

        action = action.lower()

        if action == "buy":
            cost = price * amount
            fee = cost * self.fees
            total_cost = cost + fee

            #Checking if we have sufficient balance
            if self.balance["USDT"] >= total_cost:
                self.balance["USDT"] -= total_cost
                self.balance["BTC"] += amount
                status="SUCCESS"
            else:
                print("Failed-Insufficient Balance")
                status = "Failed-IBalance"


        elif action == "sell":
            revenue = price * amount
            fee = revenue * self.fees
            total_revenue = revenue - fee

            #Checking if we have enough bitcoin
            if self.balance["BTC"] >= amount:
                self.balance["BTC"] -= amount
                self.balance["USDT"] += total_revenue
                status="SUCCESS"
            else:
                print("Failed-Insufficient Bitcoin")
                status = "Failed-IBitcoin"

        self.trade_logs.append({
            "Time": timestamp,
            "Action": action,
            "Exchange": exchange_name,
            "Price": price,
            "Amount": amount,
            "Status": status,
            "Balance_USDT": self.balance["USDT"],
            "Balance_BTC": self.balance["BTC"],
        })

        return status







