from os import pipe
from requests.api import request
# from requests_html import HTMLSession
import website
from website import Website
import pdfx
import requests
import time
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import re
from selenium.common.exceptions import WebDriverException


months={"January":"01","February":"02","March":"03","April":"04","May":"05","June":"06","July":"07","August":"08","September":"09","October":"10","November":"11","December":"12"}
months_short={"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}

project_list=[
    ["http://investor.weyerhaeuser.com/events-and-presentations",0,"item wd_event",1,"item_date wd_event_sidebar_item wd_event_date"],
    ["https://investor.fb.com/investor-events/",1,"left",0,"ModuleDateContainer"],
    ["https://informacioncorporativa.entel.cl/investors/presentations",2,"tabs tabs-style-flip",0,""],
    ["http://ir.homedepot.com/events-and-presentations",3,"snapdown-content member-description clearfix",0,"event-date-simple"]
]

domain=""
def strip_title(str):
    val=str
    str=re.sub('\n','',str)
    str=re.sub('file','',str)
    str=str.replace('(PDF)','')
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
            date=item[2]
            item[0]=strip_title(item[0])
            if(link is not None and sub in link and item[0] != ''):
                present_pdf=[]
                present_pdf.append(item[0])
                if("https" not in link):
                    link=domain+link
                present_pdf.append(link)
                present_pdf.append(date)
                pdfs.append(present_pdf)
    return pdfs


def scrap_selenium(url,first_class,date_class):
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
        date=""
        if(row.find(class_=date_class)):
            date=row.find(class_=date_class).text
            date=strip_title(date)
        for hrefs in row.find_all('a'):
            box=[]
            url_link=hrefs.get('href')
            url_title=hrefs.get_text()
            box.append(url_title)
            box.append(url_link)
            box.append(date)
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
                date=""
                if(row.find(class_=date_class)):
                    date=row.find(class_=date_class).text
                    date=strip_title(date)
                for hrefs in row.find_all('a'):
                    box=[]
                    url_link=hrefs.get('href')
                    url_title=hrefs.get_text()
                    box.append(url_title)
                    box.append(url_link)
                    box.append(date)
                    links.append(box)

    browser.close()
    return links

def scrap_normal(url,first_class,date_class):
    list_urls=[]
    request=requests.get(url)
    soup=BeautifulSoup(request.content,'html.parser')
    for item in soup.find_all('div',class_=first_class):
        date=item.find('div',class_=date_class).text
        # print(date)
        for links in item.find_all('a'):
            present_url=links.get('href')
            combo=[]
            combo.append(date)
            combo.append(present_url)
            list_urls.append(combo)
    return list_urls

def scrap_twice(url,first_class,date_class):
    list_urls=[]
    first_list_urls=scrap_normal(url,first_class,date_class)
    for link in first_list_urls:
        r=requests.get(link[1])
        date=link[0]
        soup=BeautifulSoup(r.content,'html.parser')
        for item in soup.find_all('a'):
            if(item):
                pdf=[]
                pdf.append(item.get_text())
                pdf.append(item.get('href'))
                pdf.append(date)
                list_urls.append(pdf)
    return list_urls



def scrap(url,position,first_class,depth,date_class):
    x=position
    website=Website(url,position,first_class,depth,date_class)

    mc=MongoClient()
    db=mc['scraps']
    collection_pdfs=db['scrap_items']

    website.print_data()

    global domain
    domain="https://"
    domain+=get_domain(url)

    lists=[]
    if(x==0):
        first_list=scrap_twice(website.url,website.first_class,date_class)
        lists=get_pdf_links(first_list)
    else:
        lists=(get_pdf_links(scrap_selenium(website.url,website.first_class,date_class)))
        
    for item in lists:
        if(x==0):
            date=item[2]
            box=date.split(',')
            month=box[1]
            month=month.strip()
            cube=month.split(' ')
            month=cube[0]
            year=box[2].strip()
            date=year+(months[month])
            item[2]=date
        elif(x==1):
            date=item[2]
            box=date.split(',')
            month=box[0]
            cube=month.split(' ')
            month=cube[0]
            month=months_short[month]
            year=box[1].strip()
            year=year[0:4]
            date=year+month
            item[2]=date
            item[0]+=("_"+date)
        elif(x==2):
            pdf=pdfx.PDFx(item[1])
            date=pdf.get_metadata().get("CreationDate")
            present_pdf_link=item[1]
            box=[]
            box=present_pdf_link.split('/')
            present_pdf_name=box[-1]
            item[0]=present_pdf_name
            box=date[2:8]
            item[2]=box
        else:
            s=item[1]
            s=s.replace(' ','%20')
            item[1]=s
            if(item[2]==''):
                try:
                    pdf=pdfx.PDFx(item[1])
                    date=pdf.get_metadata().get("CreationDate")
                    item[2]=date[2:8]
                except:
                    print("Broken Link")
            else:
                date=item[2]
                box=date.split(',')
                month=box[1]
                month=month.strip()
                cube=month.split(' ')
                month=cube[0]
                year=box[2]
                year=year.strip()
                year=year[0:4]
                item[2]=year+(months[month])
        # print(item[2])
    for item in lists:
            # print(item)
            collection_pdfs.update_one({'pdf_link':item[1]},{"$set":{'company_code':website.position,'pdf_name':item[0],'pdf_date':item[2]}},upsert=True)

def main_scraper():
    for i in range(0,4):
        x=i
        scrap(project_list[x][0],project_list[x][1],project_list[x][2],project_list[x][3],project_list[x][4])
        print("**************************************************")

