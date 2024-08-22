from django.shortcuts import render

from jd_loginclient.settings import BASE_URL

# api key 37137910e7013447be23a109e25d0d5ce32253bb
from django.urls.resolvers import URLResolver
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def get_url():
    from jd_loginclient.urls import urlpatterns
    urls = {}

    for i in urlpatterns:
        if type(i) != URLResolver and i.name != None:
            urls[i.name] = BASE_URL + str(i.pattern)

    return urls


class GetUrl_Api(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        urls = get_url()
        return Response(urls)
    

def test_view(request):
    import requests

    api_key = "37137910e7013447be23a109e25d0d5ce32253bb"

    headers = {
        'Authorization': f'Token 37137910e7013447be23a109e25d0d5ce32253bb'
    }

    url = "http://127.0.0.1:8001/geturl/"
    response = requests.get(url=url, headers=headers)

    from colorama import Fore
    print(Fore.GREEN + str(response.json) + Fore.WHITE)

    return render(request, "main/index.html")
