from ctypes.wintypes import SHORT
from re import template
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlencode
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from random import choice
import string
from urllib.parse import urlparse, quote, unquote
import validators
from .models import ShortenedURL

SHORTEN_LENGTH = 7

def generate_random_characters(length=SHORTEN_LENGTH):
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(length))

@require_http_methods(['GET', 'POST'])
def url_shorten(request):
    template_args = {}
    if request.method == 'POST':
        provided_url = request.POST.get('provided-url')
        is_valid = validators.url(provided_url)
        if isinstance(is_valid, validators.ValidationFailure):
            # Given url is not valid inform the user
            # Validation can be improved the give additional details of why this url is not valid
            # Additionally, duplication (in search) from the valid url can be combined to a helper function
            template_args = {
                'error': True,
                'provided_url': provided_url,
            }
        else:
            shortened_url = ShortenedURL(
                original_url=provided_url,
                shortened_identifier=generate_random_characters()
            )
            shortened_url.save()

            template_args = {
                'shortened_url': shortened_url.get_shortened_url(),
                'quoted_shortened_url': quote(shortened_url.get_shortened_url()),
                'provided_url': shortened_url.original_url,
            }
    return render(request, 'shorten.html', template_args)


@require_http_methods(['GET'])
def url_lookup(request):
    searched_url_param = request.GET.get('searched-url')
    template_args = {}

    if searched_url_param:
        searched_url = unquote(searched_url_param)
        template_args['searched_url'] = searched_url
        is_valid = validators.url(searched_url)
        if isinstance(is_valid, validators.ValidationFailure):
            template_args['error'] = 'Searched URL is not valid'
        else:
            parsed_url_info = urlparse(searched_url)
            try:
                short_identifier_for_url = parsed_url_info.path[1:]
                retrieved_url = ShortenedURL.objects.get(shortened_identifier=short_identifier_for_url)
                template_args['retrieved_url'] = retrieved_url.get_details()
            except ShortenedURL.DoesNotExist:
                template_args['error'] = 'There is no matching url'

    return render(request, 'search.html', template_args)