import requests
from twilio.rest import Client

STOCK_API_KEY = "YOUR STOCK API"
NEWS_API = "YOUR NEW API"
TWILIO_SID = "YOUR TWILIO SID"
TWILIO_AUTH = "YOUR TWILIO AUTH"

STOCK_NAME = "TSLA"
COMPANY_NAME = "tesla inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY

}
request = requests.get(STOCK_ENDPOINT,params=parameters)
data = request.json()["Time Series (Daily)"]
print(data)
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing = yesterday_data["4. close"]
print(yesterday_closing)

day_before_data = data_list[1]
day_before_close = day_before_data["4. close"]
print(day_before_close)

difference = float(yesterday_closing) - float(day_before_close)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


diff_percentage = round(difference / float(yesterday_closing)*100)
print(diff_percentage)

if abs(diff_percentage) > 1:
    news_params = {
        "apiKey":NEWS_API,
        "qInTitle": COMPANY_NAME,

    }
    news_request = requests.get(NEWS_ENDPOINT,params=news_params)
    articles= news_request.json()["articles"]
    # print(articles)

    three_articles = articles[:3]
    print(three_articles)

    formatted_article =[f"{STOCK_NAME}:{up_down}{diff_percentage}%\nHeadline:{article['title']}.\nBrief: {article['description']}" for article in three_articles]
    print(formatted_article)
    client = Client(TWILIO_SID,TWILIO_AUTH)

    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_="+YOUR TWILIO PH NO",
            to="YOUR NUMBER"
        )