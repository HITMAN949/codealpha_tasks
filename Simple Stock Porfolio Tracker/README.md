# 📊 Stock Portfolio Tracker

A command-line Python application built as part of the **Code Alpha Python Programming Internship**, designed to track and manage stock portfolios using real-time data from **Yahoo Finance** and **Alpha Vantage**.

---

## 🧠 About the Project

This project was developed during my internship at **Code Alpha** under the Python Programming track. It demonstrates practical usage of:

- API integration
- Data handling with pandas
- Real-time data fetching
- Data visualization with matplotlib
- File I/O (JSON)
- Object-oriented programming in Python

---

## 🔧 Features

- ✅ Add, update, or remove stock positions
- 📈 View detailed summaries with gain/loss
- 🔄 Toggle between Yahoo Finance and Alpha Vantage
- 🧠 Save/load your portfolio to/from JSON files
- 📊 Plot a pie chart of your portfolio composition

---

## 🛠️ Technologies Used

- `Python 3.9+`
- `yfinance`
- `pandas`
- `matplotlib`
- `requests`
- `dotenv`

---

## 🚀 How to Run

1. Clone the repo:
```bash
git clone https://github.com/yourusername/stock-portfolio-tracker.git
cd simple-stock-portfolio-tracker

## 2. Install dependencies:
```bash
pip install -r requirements.txt

## 3. Create a .env file and add your Alpha Vantage API key:

ALPHA_VANTAGE_API_KEY=your_api_key_here

##4. Run the app:
```bash
python tracker.py