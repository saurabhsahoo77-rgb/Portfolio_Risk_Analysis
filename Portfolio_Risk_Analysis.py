# Importing required libraries
import yfinance as yf        # For fetching historical stock price data
import numpy as np            # For numerical computations
from scipy.stats import norm  # For normal distribution (used in parametric VaR)
import matplotlib.pyplot as plt
import seaborn as sns         # For better-looking charts


class PortfolioRiskAnalysis:
    def __init__(self, tickers, start_date, end_date, weights):
        # Initialize the portfolio parameters
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.weights = np.array(weights)

    def download_data(self):
        """
        Download adjusted close prices for the given tickers and date range.
        Filters out tickers with no available data.
        """
        valid_tickers = []
        for ticker in self.tickers:
            try:
                data = yf.download(ticker, self.start_date, self.end_date, progress=False)
                if not data.empty:
                    valid_tickers.append(ticker)
                else:
                    print(f"⚠️ Skipping {ticker} — no data found.")
            except Exception as e:
                print(f"⚠️ Error downloading {ticker}: {e}")

        if not valid_tickers:
            raise ValueError("No valid tickers found. Please check ticker symbols.")

        # Return only closing prices for valid tickers
        return yf.download(valid_tickers, self.start_date, self.end_date, progress=False)['Close']

    def calculate_returns(self):
        """
        Calculate daily log returns for each stock in the portfolio.
        """
        data = self.download_data()
        log_returns = np.log(data / data.shift(1))
        return log_returns.dropna()

    def assign_weights(self):
        """
        Calculate the portfolio’s daily returns using asset weights.
        """
        returns = self.calculate_returns()
        portfolio_returns = returns.dot(self.weights)
        return portfolio_returns

    def var_para(self, confidence_level):
        """
        Parametric VaR (Value at Risk) assuming normal distribution.
        VaR = mean - z_score * std_dev
        """
        portfolio_returns = self.assign_weights()
        mean = portfolio_returns.mean()
        std = portfolio_returns.std()
        var = mean - (std * norm.ppf(confidence_level))
        return var

    def var_hist(self, confidence_level):
        """
        Historical VaR based on actual portfolio return distribution.
        """
        return np.percentile(self.assign_weights(), (1 - confidence_level) * 100)

    def cvar(self, confidence_level):
        """
        Conditional VaR (Expected Shortfall):
        Average loss beyond the VaR threshold.
        """
        portfolio_returns = self.assign_weights()
        var_cutoff = self.var_hist(confidence_level)
        return portfolio_returns[portfolio_returns <= var_cutoff].mean()

    def stress_testing(self, stress_scenario):
        """
        Stress testing:
        Estimate portfolio impact under a user-defined shock scenario.
        Example input: [-0.05, -0.02, -0.03] for 5%, 2%, and 3% shocks.
        """
        return np.sum(self.weights * stress_scenario)

    def chart(self):
        """
        Plot the portfolio return distribution with VaR and CVaR lines.
        """
        sns.histplot(self.assign_weights(), bins=50, kde=True)
        plt.axvline(self.var_hist(0.95), color='r', linestyle='--', label="VaR (95%)")
        plt.axvline(self.cvar(0.95), color='g', linestyle='--', label="CVaR (95%)")
        plt.legend()
        plt.title("Portfolio Return Distribution")
        plt.show()

    def menu(self):
        """
        Simple CLI menu to interact with the analysis tool.
        """
        print("\nWelcome to Portfolio Risk Analysis Tool")
        print("Select an option:")
        print("1. VaR Historic")
        print("2. VaR Parametric")
        print("3. CVaR")
        print("4. Stress Testing")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number (1–5).")
            return self.menu()

        if choice == 1:
            confidence_level = float(input("Enter confidence level (e.g. 0.95): "))
            print("VaR Historic =", round(self.var_hist(confidence_level) * 100, 2), "%")
            self.chart()

        elif choice == 2:
            confidence_level = float(input("Enter confidence level (e.g. 0.95): "))
            print("VaR Parametric =", round(self.var_para(confidence_level) * 100, 2), "%")
            self.chart()

        elif choice == 3:
            confidence_level = float(input("Enter confidence level (e.g. 0.95): "))
            print("CVaR =", round(self.cvar(confidence_level) * 100, 2), "%")
            self.chart()

        elif choice == 4:
            stress_scenario = input("Enter stress scenario (comma-separated, e.g. -0.05,-0.03,-0.02): ")
            stress_values = np.array([float(x.strip()) for x in stress_scenario.split(',')])
            print("Stress Testing =", round(self.stress_testing(stress_values) * 100, 2), "%")
            self.chart()

        elif choice == 5:
            print("Thank you for using the Portfolio Risk Analysis Tool.")
            return

        else:
            print("Invalid choice. Please select a valid option.")

        # Loop back to menu after completing an action
        self.menu()


# ------------------- Program Entry Point -------------------

print("Welcome to Portfolio Risk Analysis Tool")

# Collect portfolio details from user input
stocks = input("Enter stock tickers (comma-separated, e.g. INFY.NS, RELIANCE.NS): ")
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")
weights = input("Enter portfolio weights (comma-separated, e.g. 0.25, 0.25, 0.25, 0.25): ")

# Clean up ticker names and convert weights
stocks_list = [s.strip().replace("'", "").replace('"', "") for s in stocks.split(',')]
weights_list = [float(w.strip()) for w in weights.split(',')]

# Initialize and run the analysis tool
portfolio = PortfolioRiskAnalysis(stocks_list, start_date, end_date, weights_list)
portfolio.menu()
