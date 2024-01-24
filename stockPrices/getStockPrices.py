import requests
import json

api_key = "UC74YSXNEMG581WB" # Alpha Vantage API key
symbol = "GME"
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize=full"

response = requests.get(url)
data = response.json()

# extract data for 2022
prices = {}
for date, info in data["Time Series (Daily)"].items():
    if date.startswith("2022"):
        prices[date] = info["4. close"]

# save data to a JSON file
with open((symbol + '_prices_2022.json'), "w") as f:
    json.dump(prices, f)
