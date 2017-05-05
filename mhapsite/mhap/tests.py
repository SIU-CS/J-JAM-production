from django.test import TestCase,Client
from django.urls import reverse
from mhap.models import Quote
from mhap.models import Profile
from mhap.bot_helper import Bot
# Create your tests here.

class AppViewTest(TestCase):

    def test_home_page_redirect(self):
        response = self.client.get(reverse('mhap:index'))
        self.assertEqual(response.status_code,302)

    def test_create_page_redirect(self):
        response = self.client.get(reverse('mhap:create'))
        self.assertEqual(response.url,'/login/?next=/mhap/create/')
        
    def test_list_page_redirect(self):
        response = self.client.get(reverse('mhap:list'))
        self.assertEqual(response.url,'/login/?next=/mhap/list/')
        
    def test_bot_page_redirect(self):
        response = self.client.get(reverse('mhap:bot_page'))
        self.assertEqual(response.url,'/login/?next=/mhap/bot/')
        
    def test_settings_page_redirect(self):
        response = self.client.get(reverse('mhap:settings'))
        self.assertEqual(response.url,'/login/?next=/mhap/settings/')
    
    def test_change_password_page_redirect(self):
        response = self.client.get(reverse('mhap:change_password'))
        self.assertEqual(response.url, '/login/?next=/mhap/settings/password/')

class QuoteTest(TestCase):
    def setUp(self):
        Quote.objects.create(quote="quote",author="author")

    def test_quote_created(self):
        default_quote = Quote.objects.get(quote="quote")
        self.assertEqual(default_quote.quote,"quote")
        self.assertEqual(default_quote.author,"author")

class BotTest(TestCase):
    def test_process_message_help(self):
        help_response = Bot.process_message("help")
        self.assertEqual(help_response, Bot.help_response)
    
    def test_process_message_default(self):
        default_response = Bot.process_message("some other pattern")
        expected_response = "I am not a very intelligent bot. Please ask the MHAP team to upgrade me"
        self.assertEqual(default_response, expected_response)


# class ProfileTest(TestCase):
#     def setUp(self):
#         Profile.objects.create(user)
