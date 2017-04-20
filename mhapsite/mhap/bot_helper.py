import requests,json

from .models import Quote

#http://stackoverflow.com/questions/1859959/python-static-methods-how-to-call-a-method-from-another-method  
#http://stackoverflow.com/questions/3434581/accessing-a-class-member-variables-in-python
#http://stackoverflow.com/questions/740287/how-to-check-if-one-of-the-following-items-is-in-a-list
class Bot(object):
    'Bot Logic in a class'
    help_patterns = ['help','please help me']

    quote_patterns= ['quote','quotes','inspiration']

    help_response=['https://www.adaa.org/tips-manage-anxiety-and-stress','http://tinybuddha.com/']


    @staticmethod
    def fetch_quote(API="http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"):
        try:
            quote_json = requests.get(API).text
            quote_json = quote_json.replace('\\x', '\\u00')
            quote_json = json.loads(quote_json,strict=False)
            return (str(quote_json['quoteText']), str(quote_json['quoteAuthor']))
        except Exception as e:
            print e

        first_quote = Quote.objects.get(id=1)

        return first_quote.quote,first_quote.author

        

    @classmethod
    def process_message(cls,user_message):
    
        if type(user_message) is not str:
            return "I only accept strings"
        
        splitted_message = user_message.split(" ")
        print splitted_message
        if any(message in cls.quote_patterns for message in  splitted_message):
            return cls.fetch_quote()
            #return "You want a quote :)"

    
        elif any(message in cls.help_patterns for message in  splitted_message):
            return cls.help_response
        else:
            return "I am not a very intelligent bot. Please ask the MHAP team to upgrade me"

 


#print Bot.process_message("quote")


#print Bot.process_message("Cant interpret this")