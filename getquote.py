import requests

API="http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"

quote_json=requests.get(API).json()

print quote_json['quoteText']
print quote_json['quoteAuthor']

