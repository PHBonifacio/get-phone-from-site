from ast import Return
from os import link
import re
import threading

import requests
from bs4 import BeautifulSoup

DOMAIN = 'https://django-anuncios.solyd.com.br'
URL = "https://django-anuncios.solyd.com.br/automoveis/"

PHONES_LIST = []
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

def GetPhones(ad_description):
    if not ad_description:
        return

    phone = re.findall(r"\(?([1-9]{2})\)?[ \.\-]{0,2}(9\d{4})[ \.\-]?(\d{4})", ad_description)
    return phone

def ProcessSite(links_list):
    while True:
        try:
            link = links_list.pop(0)
        except:
            print("Error, finishing")
            return
        
        url = GetURL(DOMAIN + link)
        soap = ParseHTML(url)
        phones = GetPhones(GetAdDescription(soap))
        
        if phones:
            for phone in phones:
                PHONES_LIST.append(phone)
                print(phone)

def SaveList2File(filename, list):
    file = open(filename, "w+")
    for phone in list:
        text = "{} {}-{}\n".format(phone[0], phone[1], phone[2])
        file.write(text)    
    file.close() 

if __name__ == "__main__":    
    url = GetURL(URL)
    soup = ParseHTML(url)
    links = GetLinks(soup)
    
    threads = []
    for i in range (3):
        thread = threading.Thread(target=ProcessSite, args=(links,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    SaveList2File("phones.txt", PHONES_LIST)

    