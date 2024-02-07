import requests
from datetime import datetime
import smtplib
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    # "interval":"60min",
    "apikey":"0KUJ8E6087IRROAN"
}

time = datetime.now()
todate = int(time.day)
totime = time.hour
m = time.month
if m < 10:
    m=f"0{m}"
n=todate-2
day = "2024-01-18 12:00:00"
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get("https://www.alphavantage.co/query", params=parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
# day1 = float(data["Time Series (60min)"][f"2024-{m}-{n} 12:00:00"]["4. close"])
day1 = float(data_list[0]["4. close"])
day2 = float(data_list[1]["4. close"])
# day2 = float(data["Time Series (60min)"][f"2024-{m}-{n-1} 12:00:00"]["4. close"])
# print(day1)
# print(day2)
diff = day1 - day2
# print(diff)
if diff < 0:
    diff = diff * -1
    percent = diff/day1 * 100
    per = f"🔻 {round(percent,2)}%"
else:
    percent = diff / day1 * 100
    per = f"🔺 {round(percent,2)}%"
print(percent)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
parameter = {
    "qInTitle":COMPANY_NAME,
    # "searchin":COMPANY_NAME,
    "language":"en",
    "apiKey":"a701363ca0f74e4f8e2c410d1717c9fe"
}

if percent > 0:
    respond = requests.get("https://newsapi.org/v2/everything", params=parameter)
    news_data = respond.json()
    n = 0


    stock = f"TSLA: {per}"
    print(stock)
    three_articles = news_data["articles"][:3]
    # for i in news_data["articles"]:
    #     if n < 3:
    #         title = i["title"]
    #         message = i["description"]
    #
    #         print(f"Headline: {title}.\n Brief: {message}.\n")
    #         n += 1
    list_articles = [f"Headline: {i['title']}.\n Brief: {i['description']}.\n" for i in three_articles]
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="happinessjoseph065@gmail.com", password="egohappy065")
        for i in list_articles:
            connection.sendmail(from_addr="happinessjoseph065@gmail.com", to_addrs="happinessjoseph065", msg=f"Subject :{stock}\n\n Body:{i}")
# if totime == 0:
#     n=0
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this:
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# """

