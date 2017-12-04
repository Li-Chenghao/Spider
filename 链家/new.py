# -*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import sys
import csv

def get_urls(url):
    time.sleep(2)
    try:
        html = urlopen(url).read()
    except HTTPError as e:
        print(e)
        return None
    try:
        soup = BeautifulSoup(html,'lxml')
        links_undone = soup.select('#house-lst > li > div.info-panel > h2 > a')
    except AttributeError as e:
        return None
    return links_undone
    
def get_content(url):
    time.sleep(2)
    try:
        html = urlopen(url).read()
    except HTTPError as e:
        print(e)
        return None
    try:
        soup = BeautifulSoup(html,'lxml')
        title = soup.select('body > div.zf-top > div.title-wrapper > div > div.title > h1')[0].text
        price = soup.select('body > div.zf-top > div.cj-cun > div.content.forRent > div.houseInfo > div.price > div')[0].text
        form = soup.select('body > div.zf-top > div.cj-cun > div.content.forRent > div.houseInfo > div.room > div')[0].text
        area = soup.select('body > div.zf-top > div.cj-cun > div.content.forRent > div.houseInfo > div.area > div')[0].text       
        floor = soup.select('body > div > div > div > table > tr:nth-of-type(1) > td:nth-of-type(2)')[0].text
        direction = soup.select('body > div.zf-top > div.cj-cun > div.content.forRent > table.aroundInfo > tr:nth-of-type(1) > td:nth-of-type(4)')[0].text.split()[0]
        square = soup.select('body > div.zf-top > div.cj-cun > div.content.forRent > table >  tr:nth-of-type(2) > td:nth-of-type(2)')[0].text
        district = soup.select('body > div.zf-top > div.cj-cun > div.content.forRent > table >  tr:nth-of-type(3) > td:nth-of-type(2) > p > a')[0].text
        address = soup.select('body > div.zf-top > div.cj-cun > div.content.forRent > table > tr:nth-of-type(4) > td:nth-of-type(2) > p')[0].text.split()[0]
        data = [title, price, form, floor, direction, square, district, address]       
    except AttributeError as e:
        return None
    return data

if __name__ == '__main__':
    links = ['http://sh.lianjia.com/zufang/d{}'.format(str(i)) for i in range(1,101)]
    all_data = []
    for url in links:
        next_urls = get_urls(url)
        print(len(next_urls))
        for i in next_urls:
            link = 'http://sh.lianjia.com' + i.get('href')
            data = get_content(link)
            all_data.append(data)
            print(len(all_data))
    with open('~/data.csv','w') as f:
        csvfile = csv.writer(f)
        csvfile.writerow(['标题','价格','样式','楼层','朝向','面积','小区','地址'])
        csvfile.writerows(all_data)
        
        

