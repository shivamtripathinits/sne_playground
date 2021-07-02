from requests.api import request
# from requests_html import HTMLSession
import website
from website import Website

import requests
import time
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import re
from selenium.common.exceptions import WebDriverException

project_list=[
    ["http://investor.weyerhaeuser.com/events-and-presentations",0,"wd_events",1],
    ["https://investor.fb.com/investor-events/",1,"ModuleContainerInner events-items",0],
    ["https://informacioncorporativa.entel.cl/investors/presentations",2,"tabs tabs-style-flip",0],
    ["http://ir.homedepot.com/events-and-presentations",3,"container-fluid event-presentation-container",0]
]

domain=""
def strip_title(str):
    val=str
    str=re.sub('\n','',str)
    str=re.sub('file','',str)
    str=str.strip()
    return str

def get_domain(url):
    domain = urlparse(url).netloc
    return domain

def get_pdf_links(list):
    pdfs=[]
    sub='.pdf'
    for item in list:
        if(item is not None):
            link=item[1]
            item[0]=strip_title(item[0])
            if(link is not None and sub in link and item[0] != ''):
                present_pdf=[]
                present_pdf.append(item[0])
                if("https" not in link):
                    link=domain+link
                present_pdf.append(link)
                pdfs.append(present_pdf)
    return pdfs


def scrap_selenium(url,first_class):
    links=[]

    options=webdriver.ChromeOptions()
    options.headless=True
    browser = webdriver.Chrome(executable_path="./drivers/chromedriver",options=options)

    # browser = webdriver.Chrome(executable_path="./drivers/chromedriver",options=options)
    browser.get(url)
    time.sleep(1)

    html=browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    for row in soup.find_all('div',class_=first_class):
        for hrefs in row.find_all('a'):
            box=[]
            url_link=hrefs.get('href')
            url_title=hrefs.get_text()
            box.append(url_title)
            box.append(url_link)
            links.append(box)

    for page in soup.find_all('li',class_="pagerlink"):
        if(page.find('a')):
            next_page_url=""
            next_page_url=page.find('a').get('href')
            next_page_url=domain+next_page_url
            browser.get(next_page_url)
            time.sleep(1)
            html=browser.page_source
            soup = BeautifulSoup(html, "html.parser")
            for row in soup.find_all('div',class_=first_class):
                for hrefs in row.find_all('a'):
                    box=[]
                    url_link=hrefs.get('href')
                    url_title=hrefs.get_text()
                    box.append(url_title)
                    box.append(url_link)
                    links.append(box)

    browser.close()
    return links

def scrap_normal(url,first_class):
    list_urls=[]
    request=requests.get(url)
    soup=BeautifulSoup(request.content,'html.parser')
    for item in soup.find_all('div',class_=first_class):
        for links in item.find_all('a'):
            present_url=links.get('href')
            list_urls.append(present_url)
    return list_urls

def scrap_twice(url,first_class):
    list_urls=[]
    first_list_urls=scrap_normal(url,first_class)
    for link in first_list_urls:
        r=requests.get(link)
        soup=BeautifulSoup(r.content,'html.parser')
        for item in soup.find_all('a'):
            if(item):
                pdf=[]
                pdf.append(item.get_text())
                pdf.append(item.get('href'))
                list_urls.append(pdf)
    return list_urls



def scrap(url,position,first_class,depth):
    x=position
    website=Website(url,position,first_class,depth)

    mc=MongoClient()
    db=mc['scraps']
    collection_pdfs=db['scrap_items']

    website.print_data()

    global domain
    domain="https://"
    domain+=get_domain(url)

    lists=[]
    if(x==0):
        first_list=scrap_twice(website.url,website.first_class)
        lists=get_pdf_links(first_list)
    else:
        lists=(get_pdf_links(scrap_selenium(website.url,website.first_class)))
        if(x==2):
            for item in lists:
                present_pdf_link=item[1]
                box=[]
                box=present_pdf_link.split('/')
                present_pdf_name=box[-1]
                item[0]=present_pdf_name
    
    for item in lists:
            # print(item)
            collection_pdfs.update_one({'pdf_link':item[1]},{"$set":{'company_code':website.position,'pdf_name':item[0]}},upsert=True)

def main_scraper():
    for i in range(0,4):
        x=i
        scrap(project_list[x][0],project_list[x][1],project_list[x][2],project_list[x][3])
