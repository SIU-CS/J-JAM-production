from django.test import TestCase,Client
from django.urls import reverse
from mhap.models import Quote
# Create your tests here.

class AppViewTest(TestCase):

    def test_home_page_redirect(self):
        response = self.client.get(reverse('mhap:index'))
        self.assertEqual(response.status_code,302)

    def test_create_page_redirect(self):
        response = self.client.get(reverse('mhap:create'))
        self.assertEqual(response.url,'/login/?next=/mhap/create/')

class QuoteTest(TestCase):
    def setUp(self):
        Quote.objects.create(quote="quote",author="author")

    def test_quote_created(self):
        default_quote = Quote.objects.get(quote="quote")
        self.assertEqual(default_quote.quote,"quote")
        self.assertEqual(default_quote.author,"author")