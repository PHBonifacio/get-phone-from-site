from os import link
import requests
from bs4 import BeautifulSoup

DOMAIN = 'https://django-anuncios.solyd.com.br'
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

def GetLinks(soup):
    if soup:
        div = soup.find('div', class_='ui three doubling link cards')
        cards = div.find_all('a', class_='card')
        links = []
        for card in cards:
            links.append(card['href'])
        
        return links

def GetAdName(soap):
    if soap:
        div = soap.find('div', class_='sixteen wide column')
        h1 = div.find('h1', class_='ui dividing header')
        return h1.text.replace('\n', '')

def GetAdDescription(soap):
    if soap:
        divs = soap.find_all('div', class_='sixteen wide column')
        for div in divs:
            if div.find('h3'):
                p = div.find('p')
                return p.text.replace('\n', '')
        
url = GetURL(URL)
soup = ParseHTML(url)
links = GetLinks(soup)

for link in links:
    url = GetURL(DOMAIN + link)
    soap = ParseHTML(url)
    ad_name = GetAdName(soap)
    ad_desc = GetAdDescription(soap)
    print("{}\n\t{}\n---------------------------------------------".format(ad_name, ad_desc))