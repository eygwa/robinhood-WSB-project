import json
import numpy as np

symbol = 'AAPL'

# Load sentiment data
with open(f'/Users/brianpellegrino/CIS400SocialMedia/socialMediaTermPeoject/sentiment_analysis_wallstreetbets_{symbol}_posts_2022.json', 'r') as f:
    sentiment = json.load(f)

# Load stock price data
with open(f'/Users/brianpellegrino/CIS400SocialMedia/socialMediaTermPeoject/stockPrices/{symbol}_prices_2022.json', 'r') as f:
    stock_prices = json.load(f)

# Initialize empty lists for daily derivatives
#sentiment_derivatives = []
sentiments = []
stock_price_derivatives = []

def dateExistsInBoth(date):
    if (date in sentiment.keys() and date in stock_prices.keys()):
        return True
    else:
        return False

# Loop through sentiment scores and calculate daily derivatives
prev_score = None
for date, scores in sentiment.items():
    if not dateExistsInBoth(date):
        # Ensure the date exists in both datasets
        continue
    if prev_score is not None:
        #derivative = (scores["positive"] - prev_score["positive"]) - (scores["negative"] - prev_score["negative"])
        #sentiment_derivatives.append(derivative)
        sentiments.append(scores["positive"] - scores["negative"])
    prev_score = scores

# Loop through stock prices and calculate daily derivatives
prev_price = None
for date, price in stock_prices.items():
    if not dateExistsInBoth(date):
        continue
    if prev_price is not None:
        derivative = float(price) - float(prev_price)
        stock_price_derivatives.append(derivative)
    prev_price = price

print(sentiments)
print('Len: ' + str(len(sentiments)))
print(stock_price_derivatives)
print('Len: ' + str(len(stock_price_derivatives)))

corr_coef = np.corrcoef(sentiments, stock_price_derivatives)[0, 1]
print('Correlation: ' + str(corr_coef))
