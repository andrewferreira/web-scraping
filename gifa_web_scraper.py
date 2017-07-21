
"""
This is a scraping program written to extract member information from 'gifa.com',
Gifa is an exhibition event organizer for businesses involved in the
import and export of metals and scrap metals.

This scraper extracts from the
member list the following details:
1. Company name
2. Address
3. Phone
4. Fax
5. Image logo
6. Description
7. Website
8. Number of Employees
9. Sales volume
10. Exported content list
11. Key company officers and their designations

The data is exported to a csv and the logos are exported as .png files.

The screenshot program saves the member website home page as a .png file.

"""

#importing the necessary modules

import requests
from bs4 import BeautifulSoup as BS
import re
import time
import urllib
import pandas as pd
import os
from selenium import webdriver
import wikipedia as wiki

#browser headers for requests

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Content-Type': 'text/html'}

#the page of the member list, we will use this to grab the urls to each member page

url = 'http://www.gifa.com/cgi-bin/md_gmtn/custom/pub/show.cgi/Web-ExhShowroom/exh_showroom?fair=GMTN2015&lang=2&oid=23530&kevent=&search_string=&tcnews=&tcprod=&username2=&tcexh=&ticket=&auto_add_exh_id_list_to_notebook=0&prod_name=&passwd1=&page_id=1&ext_search_enabled=&prod_no=&event=&username=&passwd=&auto_add_event_id_list_to_notebook=0&username1=&exh_order_by=name&exh_id=654&exh_id=2385&exh_id=802&exh_id=947&exh_id=188&exh_id=186&exh_id=987&exh_id=1344&exh_id=2441&exh_id=924&exh_id=1174&exh_id=91&exh_id=1573&exh_id=492&exh_id=1941&exh_id=1704&exh_id=1014&exh_id=442&exh_id=1143&exh_id=108&exh_show_num=10000'


r = requests.get(url, headers = head)
soup = BS(r.text, "lxml")
box = soup.find_all('div', class_ = 'box_content')
url_lst = ['http://www.gifa.com' + str(i['href']) for i in box[0].find_all('a', class_ = 'bold')]

#function to grab the tab menu details

def tab_menu(soup_n):
    t = soup_n.find('ul', class_ = 'tab_menue')
    tabs = ['www.gifa.com' + str(i['href']) for i in t.find_all('a')]

    t_tabs = t.find_all('a')

    contact_persons_url = []
    products_url = []
    news_url = []

    if len(t_tabs)>=1:
        for i in t.find_all('a'):
            if i.text.strip() == 'Contact Persons':
                contact_persons_url.append('http://www.gifa.com' + str(i['href']))
            elif i.text.strip() == 'Products':
                products_url.append('http://www.gifa.com' + str(i['href']))
            elif i.text.strip() == 'Company News':
                news_url.append('http://www.gifa.com' + str(i['href']))
                
  
                


    cp_name = []
    cp_designation = []
    products_lst = []

    if len(contact_persons_url)>0:
        
        ru = urllib.urlopen(contact_persons_url[0])
        cpsoup = BS(ru.read(), "lxml")
        
        blocks = cpsoup.find_all('div', class_ = 'contact_ext')
        
        for i in blocks:
        
            cp_name.append(' '.join([v.strip() for v in i.find('h2').text.split(" ")]))
        
            try:
                cp_designation.append(i.find('strong').text.strip())
            except Exception:
                cp_designation.append(None)
                
            
    else:
        cp_name = None
        cp_designation = None
        
    if len(products_url)>0:
        
        rm = urllib.urlopen(products_url[0])
        prsoup = BS(rm.read(), "lxml")
            
        blocks_lst = prsoup.find_all('td', class_ = 'category')
            
        try:
            products_lst = [i.span.text.strip() for i in blocks_lst]
        except Exception:
            products_lst = [i.text.strip() for i in blocks_lst]
        
    else:
        
        products_lst = None
    
    try:
        cp_name_lst = [' '.join(i.split()) for i in cp_name]
    except Exception:
        cp_name_lst = [None]
    try:
        cp_designation_lst = [' '.join(i.split()) for i in cp_designation]
    except Exception:
        cp_designation_lst = [None]
        
    if products_lst != None:
        products_lst = products_lst[1:]
        
    ret_lst = [cp_name_lst, cp_designation_lst, products_lst]
    
    return ret_lst


#function to extract and write all details to a csv

def parser(url_lst):
    
    c_name = []
    c_phone = []
    c_address = []
    c_fax = []
    c_web = []
    c_para = []
    img = []
    employee_num_lst = []
    sales_vol_lst = []
    export_content_lst = []
    foundation_year_lst = []
    cp_name_lst = []
    cp_designation_lst = []
    products_lst_lst = []
    count = 0
    
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Content-Type': 'text/html'}
    
    for m in url_lst:
        count +=1
        
        rx = urllib.urlopen(m)
        soup_n = BS(rx.read(), 'lxml')
        
        c_name.append(soup_n.find('strong').text.encode('utf-8'))
        c_name_ref = soup_n.find('strong').text
        try:
            vcard = soup_n.find('div', class_ = 'vcard').p
            if 'Fax:' in vcard.text:
                re_phone = 'Phone: (.+)Fax:'
            else:
                re_phone = 'Phone: (.+)http:'
            re_addr = str(c_name_ref) + '(.+)Phone:'
            re_fax = 'Fax:(.+)?http'
            re_web = 'http://(.+)'

            ob = re.search(re_addr, vcard.text)
            ob2 = re.search(re_phone, vcard.text)
            ob3 = re.search(re_fax, vcard.text)
            ob4 = re.search(re_web, vcard.text)

            try:
                c_address.append(ob.group(1))
            except Exception:
                c_address.append(None)
            try:
                c_phone.append(ob2.group(1))
            except Exception:
                c_phone.append(None)
            try:
                c_fax.append(ob3.group(1))
            except Exception:
                c_fax.append(None)
            try:
                c_web.append(ob4.group())
            except Exception:
                c_web.append(None)
                
        except Exception:
                c_phone.append(None)
                c_address.append(None)
                c_fax.append(None)
                c_web.append(None)
                
        try:
            c_para.append(' '.join([i.text for i in soup_n.find('div', class_ = 'profile text').find_all('p')]))
        except Exception:
            c_para.append(None)
            
        try:
            prof = soup_n.find('div', class_ = 'profile text')
            img.append('http://www.gifa.com' + str(prof.img['src']))
        except Exception:
            img.append(None)
            
        
        try:
            cf = soup_n.find('div', class_ = "exh_videos additional_info").find_all('td')
            cf_lst = [i.text for i in cf]
            employee_num = []
            foundation_year = []
            export_content = []
            sales_vol = []
            for i in cf_lst:
                if 'Mio' in i or '$' in i:
                    sales_vol.append(i)
                elif '%' in i:
                    export_content.append(i)
                elif len(i) == 4 and '-' not in i:
                    foundation_year.append(i)
                elif i != 'Company Figures' and i != 'Year of foundation' and i != 'Number of employees' and 'Sales volume' not in i and i != 'Export content':
                    employee_num.append(i)
                    
            gg = [employee_num, sales_vol, export_content, foundation_year]
            
            for i in gg:
                if len(i) == 0:
                    i.append(None)
                    
            employee_num_lst.append(gg[0][0])
            sales_vol_lst.append(gg[1][0])
            export_content_lst.append(gg[2][0])
            foundation_year_lst.append(gg[3][0])
                    
        except Exception:
            employee_num_lst.append(None)
            sales_vol_lst.append(None)
            export_content_lst.append(None)
            foundation_year_lst.append(None)
            
        gets = tab_menu(soup_n)
            
        cp_name_lst.append(gets[0])
        cp_designation_lst.append(gets[1])
        products_lst_lst.append(gets[2])
        
        print str(count) + ' done'
        
            
    
    df = pd.DataFrame()
    
    df['company'] = c_name
    df['address'] = c_address
    df['company phone'] = c_phone
    df['company fax'] = c_fax
    df['company website'] = c_web
    df['about us'] = c_para
    df['shared image url'] = img
    df['number of employees'] = employee_num_lst
    df['sales volume (in K)'] = sales_vol_lst
    df['export content'] = export_content_lst
    df['Year of Foundation'] = foundation_year_lst
    df['Key People'] = cp_name_lst
    df['Designations'] = cp_designation_lst
    df['Products'] = products_lst_lst
    
    df.to_csv('gifa.csv', encoding= 'utf-8')
    
    return df

#function to create screenshots of member websites

def screenshot(url_list, c_list):
    count = 0
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768) 
    for i,b in zip(url_list, c_list):
        count+=1
        os.chdir('/input/desired/path/here/')
        # set the window size that you need 
        driver.get(i)
        driver.save_screenshot(str(b)+'.png')
        print str(count) + ' done'

#list of member websites

web = df[df['company website'].isnull()==False]

if __name__ == '__main__':
    parser(url_lst)
    screenshot(web['company website'], web['company'])

















