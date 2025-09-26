import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Headers to avoid HTTP 403 errors
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.90 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# Tesla stock data
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)

# Tesla revenue data
tesla_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
response = requests.get(tesla_url, headers=headers)
tables = pd.read_html(response.text)
tesla_revenue = tables[1] if len(tables) > 1 else tables[0]
tesla_revenue.columns = ["Date", "Revenue"]
tesla_revenue = tesla_revenue.dropna()

# GameStop stock data
gamestop = yf.Ticker("GME")
gme_data = gamestop.history(period="max")
gme_data.reset_index(inplace=True)

# GameStop revenue data
gme_url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
response = requests.get(gme_url, headers=headers)
tables = pd.read_html(response.text)
gme_revenue = tables[1] if len(tables) > 1 else tables[0]
gme_revenue.columns = ["Date", "Revenue"]
gme_revenue = gme_revenue.dropna()

# Plot Tesla dashboard with legend
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(tesla_data['Date'], tesla_data['Close'], 'r-', label='Tesla Stock Price')
ax1.set_xlabel('Date')
ax1.set_ylabel('TSLA Stock Price', color='red')
ax2 = ax1.twinx()
ax2.plot(
    pd.to_datetime(tesla_revenue['Date']),
    tesla_revenue['Revenue'].replace('[$,]', '', regex=True).astype(float),
    color='orange',
    label='Tesla Revenue'
)
ax2.set_ylabel('Revenue', color='orange')
plt.title("Tesla Stock Price and Revenue")
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
plt.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
plt.show()

# Plot GameStop dashboard with legend
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(gme_data['Date'], gme_data['Close'], 'b-', label='GameStop Stock Price')
ax1.set_xlabel('Date')
ax1.set_ylabel('GME Stock Price', color='blue')
ax2 = ax1.twinx()
ax2.plot(
    pd.to_datetime(gme_revenue['Date']),
    gme_revenue['Revenue'].replace('[$,]', '', regex=True).astype(float),
    'g-',
    label='GameStop Revenue'
)
ax2.set_ylabel('Revenue', color='green')
plt.title("GameStop Stock Price and Revenue")
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
plt.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
plt.show()
