"""
Contains the configuration for mhap to be plugged in mhapsite

"""

from __future__ import unicode_literals

from django.apps import AppConfig


class MhapConfig(AppConfig):
    """
        Extends AppConfig and has name of our app which is mhap
    """
    name = 'mhap'
