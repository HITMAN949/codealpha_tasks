import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os


class StockPortfolioTracker:
    def __init__(self):
        self.portfolio = {}
        self.alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY',
                                               'your_api_key')
        self.use_alpha_vantage = False

    def toggle_data_source(self):

        self.use_alpha_vantage = not self.use_alpha_vantage
        source = "Alpha Vantage" if self.use_alpha_vantage else "Yahoo Finance"
        print(f"Switched to {source} for market data")

    def get_current_price(self, symbol):

        if self.use_alpha_vantage:
            return self._get_price_alpha_vantage(symbol)
        else:
            return self._get_price_yfinance(symbol)

    def _get_price_yfinance(self, symbol):

        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            if not hist.empty:
                return hist['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"YFinance Error for {symbol}: {str(e)}")
            return None

    def _get_price_alpha_vantage(self, symbol):

        base_url = "https://www.alphavantage.co/query"
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.alpha_vantage_api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'Global Quote' in data and '05. price' in data['Global Quote']:
                return float(data['Global Quote']['05. price'])
            else:
                error_msg = data.get('Note', data.get('Information', 'Unknown error'))
                print(f"AlphaVantage Error for {symbol}: {error_msg}")
                return None
        except Exception as e:
            print(f"AlphaVantage Connection Error: {str(e)}")
            return None

    def add_stock(self, symbol: str, shares: float, purchase_price: float, purchase_date: str):

        symbol = symbol.upper()
        try:
            shares = float(shares)
            purchase_price = float(purchase_price)
            datetime.strptime(purchase_date, "%Y-%m-%d")  # Validate date format
        except ValueError as e:
            print(f"Invalid input: {e}")
            return

        if symbol in self.portfolio:

            total_shares = self.portfolio[symbol]['shares'] + shares
            total_cost = (self.portfolio[symbol]['shares'] * self.portfolio[symbol]['purchase_price']) + (
                        shares * purchase_price)
            self.portfolio[symbol]['purchase_price'] = total_cost / total_shares
            self.portfolio[symbol]['shares'] = total_shares
            print(
                f"Updated {symbol} position to {total_shares} shares at avg price ${self.portfolio[symbol]['purchase_price']:.2f}")
        else:
            self.portfolio[symbol] = {
                'shares': shares,
                'purchase_price': purchase_price,
                'purchase_date': purchase_date
            }
            print(f"Added {shares} shares of {symbol} to portfolio")

    def remove_stock(self, symbol: str, shares: float = None):

        symbol = symbol.upper()
        if symbol not in self.portfolio:
            print(f"{symbol} not in portfolio")
            return

        if shares is None or shares >= self.portfolio[symbol]['shares']:
            del self.portfolio[symbol]
            print(f"Removed all shares of {symbol}")
        else:
            self.portfolio[symbol]['shares'] -= shares
            print(f"Removed {shares} shares of {symbol}. Remaining: {self.portfolio[symbol]['shares']}")

    def portfolio_summary(self):

        if not self.portfolio:
            print("Portfolio is empty")
            return

        total_investment = 0
        total_current_value = 0
        report = []

        for symbol, data in self.portfolio.items():
            current_price = self.get_current_price(symbol)
            if current_price is None:
                print(f"Could not get price for {symbol}")
                continue

            shares = data['shares']
            cost_basis = data['purchase_price']
            investment = shares * cost_basis
            current_value = shares * current_price
            gain_loss = current_value - investment
            gain_loss_pct = (gain_loss / investment) * 100

            total_investment += investment
            total_current_value += current_value

            report.append({
                'Symbol': symbol,
                'Shares': f"{shares:.2f}",
                'Avg Cost': f"${cost_basis:.2f}",
                'Current Price': f"${current_price:.2f}",
                'Invested': f"${investment:.2f}",
                'Current Value': f"${current_value:.2f}",
                'Gain/Loss ($)': f"${gain_loss:.2f}",
                'Gain/Loss (%)': f"{gain_loss_pct:.2f}%"
            })


        total_gain_loss = total_current_value - total_investment
        total_gain_loss_pct = (total_gain_loss / total_investment) * 100 if total_investment != 0 else 0


        df = pd.DataFrame(report)
        print("\n=== PORTFOLIO DETAILS ===")
        print(df.to_string(index=False))

        print("\n=== SUMMARY ===")
        print(f"Total Invested: ${total_investment:.2f}")
        print(f"Current Value: ${total_current_value:.2f}")
        print(f"Total Gain/Loss: ${total_gain_loss:.2f} ({total_gain_loss_pct:.2f}%)")

        return {
            'total_investment': total_investment,
            'current_value': total_current_value,
            'gain_loss': total_gain_loss,
            'gain_loss_pct': total_gain_loss_pct
        }

    def plot_portfolio(self):

        if not self.portfolio:
            print("Portfolio is empty")
            return

        symbols = []
        values = []

        for symbol, data in self.portfolio.items():
            current_price = self.get_current_price(symbol)
            if current_price is None:
                continue
            symbols.append(symbol)
            values.append(data['shares'] * current_price)

        if not values:
            print("No valid data to plot")
            return

        plt.figure(figsize=(10, 6))
        plt.pie(values, labels=symbols, autopct='%1.1f%%', startangle=90)
        plt.title('Portfolio Composition by Value')
        plt.show()

    def save_portfolio(self, filename='portfolio.json'):

        try:
            with open(filename, 'w') as f:
                json.dump(self.portfolio, f, indent=2)
            print(f"Portfolio saved to {filename}")
        except Exception as e:
            print(f"Error saving portfolio: {str(e)}")

    def load_portfolio(self, filename='portfolio.json'):
        """Load portfolio from JSON file"""
        try:
            with open(filename, 'r') as f:
                self.portfolio = json.load(f)
            print(f"Portfolio loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found")
        except Exception as e:
            print(f"Error loading portfolio: {str(e)}")


def main():
    tracker = StockPortfolioTracker()

    while True:
        print("\n===== Stock Portfolio Tracker =====")
        print("1. Add/Update Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Plot Portfolio")
        print("5. Toggle Data Source (Current: " +
              ("Alpha Vantage" if tracker.use_alpha_vantage else "Yahoo Finance") + ")")
        print("6. Save Portfolio")
        print("7. Load Portfolio")
        print("8. Exit")

        choice = input("Enter choice (1-8): ").strip()

        if choice == '1':
            try:
                symbol = input("Stock symbol: ").strip().upper()
                shares = float(input("Number of shares: ").strip())
                price = float(input("Purchase price per share: ").strip())
                date = input("Purchase date (YYYY-MM-DD): ").strip()
                tracker.add_stock(symbol, shares, price, date)
            except ValueError:
                print("Invalid input. Please enter valid numbers.")

        elif choice == '2':
            symbol = input("Stock symbol to remove: ").strip().upper()
            action = input("Remove all shares? (Y/N): ").strip().upper()
            if action == 'Y':
                tracker.remove_stock(symbol)
            else:
                try:
                    shares = float(input("Number of shares to remove: ").strip())
                    tracker.remove_stock(symbol, shares)
                except ValueError:
                    print("Invalid share amount")

        elif choice == '3':
            tracker.portfolio_summary()

        elif choice == '4':
            tracker.plot_portfolio()

        elif choice == '5':
            tracker.toggle_data_source()

        elif choice == '6':
            filename = input("Filename to save (default: portfolio.json): ").strip()
            tracker.save_portfolio(filename if filename else None)

        elif choice == '7':
            filename = input("Filename to load (default: portfolio.json): ").strip()
            tracker.load_portfolio(filename if filename else None)

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    from dotenv import load_dotenv

    load_dotenv()

    main()