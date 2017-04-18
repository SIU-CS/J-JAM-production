import re


help_patterns = ['help','please help me']

quote_patterns= ['quote','quotes','inspiration']

help_response=['https://www.adaa.org/tips-manage-anxiety-and-stress','http://tinybuddha.com/']



import requests
def process_message(user_message):
    if type(user_message) is not str:
        return "WHOOPS"
    splitted_message = user_message.split(" ")
    #http://stackoverflow.com/questions/740287/how-to-check-if-one-of-the-following-items-is-in-a-list
    if any(message in help_patterns for message in  splitted_message):
        return "You want a quote :)"
    
    elif any(message in quote_patterns for message in  splitted_message):
        return "You want help :)"
    else:
        return "USAGE ['quote','quotes','inspiration'],['help','please help me']"
    


    
    
    
for help in help_patterns:
    print process_message(help)

for quote in quote_patterns:
    print process_message(quote)