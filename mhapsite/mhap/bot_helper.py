import re


help_patterns = ['help','please help me']

quote_patterns= ['quote','quotes','inspiration']

help_response=['https://www.adaa.org/tips-manage-anxiety-and-stress','http://tinybuddha.com/']



import requests

    

    #http://stackoverflow.com/questions/740287/how-to-check-if-one-of-the-following-items-is-in-a-list
class Bot(object):
    'Bot Logic in a class'
    help_patterns = ['help','please help me']

    quote_patterns= ['quote','quotes','inspiration']

    help_response=['https://www.adaa.org/tips-manage-anxiety-and-stress','http://tinybuddha.com/']

    @staticmethod
    def process_message(user_message):
    
        if type(user_message) is not str:
            return "I only accept strings"
        
        splitted_message = user_message.split(" ")

        if any(message in help_patterns for message in  splitted_message):
            return "You want a quote :)"
    
        elif any(message in quote_patterns for message in  splitted_message):
            return "You want help :)"
        else:
            return "I am not a very intelligent bot. Please ask the MHAP team to upgrade me"

    
for help in help_patterns:
    print Bot.process_message(help)

for quote in quote_patterns:
    print Bot.process_message(quote)

print Bot.process_message("Cant interpret this")