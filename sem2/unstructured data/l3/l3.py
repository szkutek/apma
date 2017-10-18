import urllib.request
from bs4 import BeautifulSoup
import networkx as nx
import itertools
import pylab
import unidecode

if __name__ == '__main__':
    url = 'http://www.gutenberg.org/cache/epub/103/pg103.txt'
    page = urllib.request.urlopen(url)
    data = page.read()  # a `bytes` object
    text = data.decode('utf-8')  # a `str`; this step can't be used if data is binary

    print(text)
    # soup = BeautifulSoup(page, 'html.parser')
