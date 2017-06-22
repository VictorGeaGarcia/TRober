import requests
from bs4 import BeautifulSoup


def BSoup(url):
#Metiendo la url obtiene directamente lo sopa de palabaras    
    soup = BeautifulSoup(requests.get(url).text)
    return soup

