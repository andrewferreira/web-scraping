

#program that extracts wikipedia table and returns dict (prints it in this case)


import wikipedia as wiki
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup as BS


def get_wiki_table(x):
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Content-Type': 'text/html'}
    try:
        b = wiki.summary(x)
        name = x
        op = [name]
    except wiki.exceptions.DisambiguationError as e:
        op = e.options
    
    name_c = re.sub(' ', '+', op[0])
    
    wiki_search = 'https://en.wikipedia.org/w/index.php?search=' +str(name_c)+'&title=Special:Search&go=Go&searchToken=447ir5zk01lq2kvlzc25b4j3j'
    
    r = requests.get(wiki_search, headers=head)
    soup = BS(r.text, 'lxml')
    
    
    vcard = soup.find('table', class_='infobox vcard')
    
 
    try:
        tr = vcard.find_all('tr')
        for i in tr:
            print i.text.strip()
    except AttributeError:
        print 'No wikipedia table available'




if __name__ == '__main__':
    get_wiki_table(raw_input('which company would you like to look up?'))

