import re


help_patterns = ['help','please help me']

quote_patterns= ['quote','quotes','inspiration']

import requests
def process_message(user_message):
    if type(user_message) is not str:
        return "WHOOPS"
    splitted_message = user_message.split(" ")
    #http://stackoverflow.com/questions/740287/how-to-check-if-one-of-the-following-items-is-in-a-list
    if any(message in help_patterns for message in  splitted_message):
        print "Found help fam"
    
    if any(message in quote_patterns for message in  splitted_message):
        print "Found quote fam"


    
    
    
for help in help_patterns:
    print process_message(help)

for quote in quote_patterns:
    print process_message(quote)