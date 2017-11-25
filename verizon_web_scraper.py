
"""
this script is made to extract all unit data on the Verizon LTE and GSM IoT
specific chipsets. The first function runs a headless browser that runs all the
ajax called details of the page and returns a list of all the product
urls.

The second function parses each urls html and returns a dataframe and csv file
containing a consolidated list of all the product details.

The following product details can be extracted using this parser:

1. company_name
2. product
3. key features 
4. product description 
5. network technology
6. LTE category support 
7. form factor 
8. UDP 
9. TCP 
10.UART 
11.GPIO
12.Serial 
13.GPS
14.LTE 
15.GPRS 
16.GSM 
17.Dimensions
18.relative humidity
19.Stored temperature 
20.operating temperature 
21.weight
22.voltage supply
23.power consumption 
24.FCC ID

"""

from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
import pandas
import requests

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Content-Type': 'text/html'}

main_url = r'https://opendevelopment.verizonwireless.com/design-and-build/approved-modules'

#function to get url list of products

def get_url_lst(url):
    lst = []
    browser = webdriver.Chrome()

    browser.get(url)
    time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    countdwn = 9

    while countdwn:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        countdwn-=1

    post_elems = browser.find_element_by_link_text('Learn more')

    for post in post_elems:
        lst.append(post.get_attribute('href'))

    return lst

#function to parse html pages and extract data to csv/dataframe

def scraper_1(lst):
    
    company_name = []
    product = []
    key_features = []
    product_description = []
    network_technology = []
    lte_category_support = []
    form_factor = []
    UDP = []
    TCP = []
    UART = []
    GPIO = []
    Serial = []
    GPS = []
    LTE = []
    GPRS = []
    GSM = []
    dimensions = []
    relative_humidity = []
    stored_temperature = []
    operating_temperature = []
    weight = []
    voltage_supply = []
    power_consumption = []
    fcc_id = []
    
    
    for item in lst:
        r = requests.get(item, headers = head)
        soup = BS(r.text, 'lxml')
        c_name = soup.find('h6', class_ = 'details__content-subtitle show-for-medium').text.strip()
        model = soup.find('h2', class_ = 'details__content-title show-for-medium').text.strip()
        key_feat = []
        
        soupy = soup.find('ul', class_ = 'details__content-list')
        key_fs = soupy.find_all('li', class_ = 'details__content-item')
        for i in key_fs:
            key_feat.append(i.text.strip())
            
        prod_desc = soup.find('p', class_ = 'details__content-copy').text.strip()
        fcc = soup.find('p', class_ = 'details__content-subhead-copy--section-break').text.strip()
        
        div_lst = soup.find_all('div', class_ = 'details__content-features')
        label = div_lst[2].find_all('dt', class_ = 'definition-list-term--normal')
        value = div_lst[2].find_all('dd', class_ = 'definition-list-description')
        overview_lst = []
        for i,v in zip(label, value):
            overview_lst.append([i.text.strip(),v.text.strip()])

        network_tech = []
        form_fact = []
        lte_cat = []
    
        for i in overview_lst:
            if i[0] == 'Network technology':
                network_tech.append(i[1])
            elif i[0] == 'Form factor':
                form_fact.append(i[1])
            elif i[0] == 'LTE category support':
                lte_cat.append(i[1])
        
        ov_lst = [network_tech, form_fact, lte_cat]
        for i in ov_lst:
            if len(i) == 0:
                i.append(None)
                
        m_label = soup.find_all('h6', class_ = 'details__image-content-copy-header')
        m_deets = soup.find_all('p', class_ = 'details__image-content-copy')
        m_deets.append(soup.find('a', class_ = 'details__image-content-copy link'))

        addr = []
        ph = []
        email = []
        manu_lst = []

        for i,v in zip(m_label, m_deets):
            manu_lst.append([i.text.strip(), v.text.strip()]) 
            
        for i in manu_lst:
            if i[0] == 'Address':
                addr.append(i[1])
            elif i[0] == 'Phone':
                ph.append(i[1])
            elif i[0] == 'Email':
                email.append(i[1])

        bigger_div_lst = soup.find_all('div', class_ ='details__content-features')    
        bigger_div_lst = bigger_div_lst[3:]

        udp = []
        tcp = []
        uart = []
        gpio = []
        serial = []
        gps = []
        lte = []
        gprs = []
        gsm = []

        hardware_lst = []

        hardware_labels = bigger_div_lst[0].find_all('dt', class_ = 'definition-list-term--normal')
        hardware_values = bigger_div_lst[0].find_all('dd', class_ = 'definition-list-description--right')

        for i,v in zip(hardware_labels, hardware_values):
            hardware_lst.append([i.text.strip(), v.text.strip()])
            
        for i in hardware_lst:
            if i[0] == 'UDP':
                udp.append(i[1])
            elif i[0] == 'TCP':
                tcp.append(i[1])
            elif i[0] == 'UART':
                uart.append(i[1])
            elif i[0] == 'GPIO':
                gpio.append(i[1])
            elif i[0] == 'Serial':
                serial.append(i[1])
            elif i[0] == 'GPS':
                gps.append(i[1])
            elif i[0] == 'LTE':
                lte.append(i[1])
            elif i[0] == 'GPRS':
                gprs.append(i[1])
            elif i[0] == "GSM":
                gsm.append(i[1])
                
        f_lst = [udp, tcp, uart, gpio, serial, gps, lte, gprs, gsm]

        for i in f_lst:
            if len(i) == 0:
                i.append(None)

        hardware_lst2 = []

        bigger_div_lst_1 = bigger_div_lst[1].find('dl', class_ = 'details__content-definition-list')

        hardware_labels2 = bigger_div_lst_1.find_all('dt', class_ = 'definition-list-term--normal')
        hardware_values2 = bigger_div_lst_1.find_all('dd', class_ = 'definition-list-description--right')

        for i,v in zip(hardware_labels2, hardware_values2):
            hardware_lst2.append([i.text.strip(), v.text.strip()])
            
        vo_capable = []
        im_client = []
        batt_safety = []
        sms_cap = []
        dev_kit = []

        for i in hardware_lst2:
            if i[0] == 'Voice capable':
                vo_capable.append(i[1])
            elif i[0] == 'Native IM client':
                im_client.append(i[1])
            elif i[0] == 'Battery safety':
                batt_safety.append(i[1])
            elif i[0] == 'SMS Capability':
                sms_cap.append(i[1])
            elif i[0] == 'Developer Kit':
                dev_kit.append(i[1])
                
        hd_lst = [vo_capable, im_client, batt_safety, sms_cap, dev_kit]
        for i in hd_lst:
            if len(i) == 0:
                i.append(None)

        hardware_lst3 = []

        bigger_div_lst_3 = bigger_div_lst[2]

        hardware_labels_3 = bigger_div_lst_3.find_all('h6', class_ = 'details__content-subheader')
        hardware_values_3 = bigger_div_lst_3.find_all('p', class_ = 'details__content-subhead-copy--short-break')

        for i,v in zip(hardware_labels_3, hardware_values_3):
            hardware_lst3.append([i.text.strip(), v.text.strip()])
            
        dimens = []
        rel_humidity = []
        stored_temp = []
        op_temp = []
        wt = []
        volt_sup = []
        power_con = []

        for i in hardware_lst3:
            if i[0] == 'Dimensions':
                dimens.append(i[1])
            elif i[0] == 'Relative humidity':
                rel_humidity.append(i[1])
            elif i[0] == 'Stored temperature':
                stored_temp.append(i[1])
            elif i[0] == 'Operating temperature':
                op_temp.append(i[1])
            elif i[0] == 'Weight':
                wt.append(i[1])
            elif i[0] == 'Voltage supply':
                volt_sup.append(i[1])
            elif i[0] == 'Power consumption':
                power_con.append(i[1])
                
        f3_lst = [dimens, rel_humidity, stored_temp, op_temp, wt, volt_sup, power_con]

        for i in f3_lst:
            if len(i) == 0:
                i.append(None)
                
        company_name.append(c_name)
        product_description.append(prod_desc)
        product.append(model)
        fcc_id.append(fcc)
        dimensions.append(dimens)
        relative_humidity.append(rel_humidity)
        stored_temperature.append(stored_temp)
        operating_temperature.append(op_temp)
        weight.append(wt)
        voltage_supply.append(volt_sup)
        power_consumption.append(power_con)
        key_features.append(key_feat)
        network_technology.append(network_tech)
        lte_category_support.append(lte_cat)
        form_factor.append(form_fact)
        UDP.append(udp)
        TCP.append(tcp)
        UART.append(uart)
        GPIO.append(gpio)
        Serial.append(serial)
        GPS.append(gps)
        LTE.append(lte)
        GPRS.append(gprs)
        GSM.append(gsm)
        
    df = pandas.DataFrame()
    
    df['company name'] = company_name
    df['product description'] = product_description
    df['product'] = product
    df['FCC ID'] = fcc_id
    df['Dimensions'] = dimensions
    df['Relative Humidity'] = relative_humidity
    df['Stored Temperature'] = stored_temperature
    df['Operating Temperature'] = operating_temperature
    df['Weight'] = weight
    df['Voltage Supply'] = voltage_supply
    df['Power Consumption'] = power_consumption
    df['Key features'] = key_features
    df['Network technology'] = network_technology
    df['LTE category support'] = lte_category_support
    df['Form factor'] = form_factor
    df['UDP'] = UDP
    df['TCP'] = TCP
    df['UART'] = UART
    df['GPIO'] = GPIO
    df['Serial'] = Serial
    df['GPS'] = GPS
    df['LTE'] = LTE
    df['GPRS'] = GPRS
    df['GSM'] = GSM
    
    df.to_csv('Product_details.csv', encoding='utf-8')
    return df


