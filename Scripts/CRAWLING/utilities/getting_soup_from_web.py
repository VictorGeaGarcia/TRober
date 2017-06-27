import requests

from bs4 import BeautifulSoup

def BSoup(url):
'''INSERTING URL RETRIEVES DIRECTLY THE NEEDED SOUP FROM HTML WEBPAGE'''
#Metiendo la url obtiene directamente lo sopa de palabaras    
    soup = BeautifulSoup(requests.get(url).text)
    return soup

