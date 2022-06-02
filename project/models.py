from django.db import models
from urllib.parse import urlparse


class ShortenedURL(models.Model):
    shortened_identifier = models.TextField(max_length=200, primary_key=True, unique=True)
    original_url = models.TextField()

    def get_shortened_url(self):
        return f'https://bit.ly/{self.shortened_identifier}'

    def get_details(self):
        parsed_url = urlparse(self.original_url)
        return {
            'original': self.original_url,
            'schema': parsed_url.scheme, 
            'domain': parsed_url.hostname,
            'path': parsed_url.path,
            'query': parsed_url.query,
        }