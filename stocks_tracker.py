import os
import requests
import pandas as pd

class Stock:
    def __init__(self, symbol, shares, purchase_price):
        self.symbol = symbol
        self.shares = shares
        self.purchase_price = purchase_price
        self.current_price = None

    def update_price(self, api_key):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={self.symbol}&interval=1min&apikey={api_key}'
        response = requests.get(url).json()
        try:
            self.current_price = float(response['Time Series (1min)'][list(response['Time Series (1min)'].keys())[0]]['4. close'])
        except KeyError:
            print(f"Error fetching data for {self.symbol}")

    def current_value(self):
        return self.shares * self.current_price

class Portfolio:
    def __init__(self):
        self.stocks = []

    def add_stock(self, symbol, shares, purchase_price):
        stock = Stock(symbol,shares,purchase_price)
        self.stocks.append(stock)
        

    def remove_stock(self, symbol):
        self.stocks = [stock for stock in self.stocks if stock.symbol != symbol]

    def update_prices(self, api_key):
        for stock in self.stocks:
            stock.update_price(api_key)

    def total_value(self):
        return sum(stock.current_value() for stock in self.stocks if stock.current_price)

    def total_investment(self):
        return sum(stock.shares * stock.purchase_price for stock in self.stocks)

    def profit_loss(self):
        return self.total_value() - self.total_investment()

    def display(self):
        data = [{'Symbol': stock.symbol, 'Shares': stock.shares, 'Purchase Price': stock.purchase_price,
                 'Current Price': stock.current_price, 'Current Value': stock.current_value()}
                for stock in self.stocks if stock.current_price]
        df = pd.DataFrame(data)
        print(df)
        print(f"Total Investment: {self.total_investment()}")
        print(f"Total Value: {self.total_value()}")
        print(f"Profit/Loss: {self.profit_loss()}")

if __name__ == "__main__":
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    portfolio = Portfolio()
    portfolio.add_stock('AAPL', 10, 150)
    portfolio.add_stock('MSFT', 5, 200)
    portfolio.update_prices(api_key)
    portfolio.display()