from django import template
import requests

register = template.Library()


@register.simple_tag()
def get_url(name=None):

    headers = {
        'Authorization': f'Token 37137910e7013447be23a109e25d0d5ce32253bb'
    }

    urls = requests.get(url="http://127.0.0.1:8001/geturl/", headers=headers).json()

    return urls