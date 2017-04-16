from django.core.management.base import BaseCommand,CommandError

from mhap.models import Quote

import requests,json

class Command(BaseCommand):
    help = "Fetches new quote by making GET request to API"

    def add_arguments(self,parser):
        parser.add_argument('secret', type=str)

    def handle(self,*args,**options):

        print "in handle"
        try:
            if options['secret'] == 'please':

                #http://stackoverflow.com/questions/18233091/json-loads-with-escape-characters
                API = "http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
                quote_json = requests.get(API).text
                quote_json = quote_json.replace('\\x', '\\u00')
                quote_json = json.loads(quote_json)
                quote_text, quote_author = quote_json['quoteText'], quote_json['quoteAuthor']

                if quote_author != "" and quote_text != "":
                    quote_two = Quote.objects.get(id=2)
                    quote_two.quote = quote_text
                    quote_two.author = quote_author
                    quote_two.save()
            else:
                raise CommandError("Invalid option to quoteupdate")
        except Exception as e:
            raise CommandError("OOPS : {}".format(e))


