# Portfolio Risk Analysis Tool

This is a simple Python project I built to analyze the risk of a stock portfolio using different Value at Risk (VaR) methods.  
It uses historical market data from Yahoo Finance to estimate potential portfolio losses at a given confidence level.  
The tool also supports Conditional VaR (Expected Shortfall) and a basic stress testing feature.

---

## What It Does

- Fetches historical price data for multiple stocks  
- Calculates daily log returns and portfolio returns  
- Computes:
  - **Parametric VaR (Normal distribution approach)**
  - **Historical VaR**
  - **Conditional VaR (CVaR)**
  - **Stress Testing** under custom shock scenarios  
- Plots the return distribution with VaR and CVaR lines marked for reference

---

## Example Use Case

If you want to check how risky your portfolio is at a 95% confidence level,  
you can enter your tickers (like `INFY.NS, RELIANCE.NS, TATASTEEL.NS`),  
start and end dates, and portfolio weights.  
The program then shows your potential loss estimate and a nice chart of the distribution.

---

## Technologies Used

- Python  
- yfinance  
- numpy  
- scipy  
- matplotlib  
- seaborn  

---

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/YourUsername/Portfolio-Risk-Analysis.git
   cd Portfolio-Risk-Analysis
