import requests
from bs4 import BeautifulSoup

URL = "https://django-anuncios.solyd.com.br/automoveis/"

def GetURL(url):
    try:
        req = requests.get(url)
        if 200 == req.status_code:
            return req.text
        else:
            print("Request Status : {}".format(req.status_code))
    except Exception as error:
        print(error)

def ParseHTML(html):
    try:
        return BeautifulSoup(html, 'html.parser')
    except Exception as error:
        print(error)


print(ParseHTML(GetURL(URL)))