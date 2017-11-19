import time
import requests
import xlsxwriter
from bs4 import BeautifulSoup
#这个爬虫爬去了58同城上海地区的二手手机中转转用户的信息



#返回每一条信息的具体链接
def get_urls_in_one_page(url,links,headers):
    html = requests.get(url,headers = headers).text
    soup = BeautifulSoup(html,'lxml')
    hrefs = soup.select('#infolist > div:nth-of-type(6) > table > tbody > tr > td.t > a')
    
    for href in hrefs:
        links.append(href.get('href'))
        
    return links
    
       
#返回货品页的具体信息 
def get_content(url,headers):
    time.sleep(2)
    html = requests.get(url,headers = headers).text
    soup = BeautifulSoup(html,'lxml')

    cla = soup.select('#nav > div > span:nth-of-type(3) > a')[0].text.strip()
    owner = soup.select('body > div.content > div > div.box_right > div:nth-of-type(1) > div.personal_jieshao > p.personal_name')[0].text
    title = soup.select('body > div.content > div > div.box_left > div.info_lubotu.clearfix > div.box_left_top > h1')[0].text
    look_time = soup.select('body > div.content > div > div.box_left > div.info_lubotu.clearfix > div.box_left_top > p > span.look_time')[0].text
    price = soup.select('body > div.content > div > div.box_left > div.info_lubotu.clearfix > div.info_massege.left > div.price_li > span > i')[0].text
    area = soup.select('body > div.content > div > div.box_left > div.info_lubotu.clearfix > div.info_massege.left > div.palce_li > span > i')[0].text

    data = {
        'cla':cla,
        'owner':owner,
        'title':title,
        'look_time':look_time,
        'price':price,
        'area':area,
        }

    return data
    
    
def write_xlsx(data,path): 

    wb = xlsxwriter.Workbook(path)
    ws = wb.add_worksheet('58同城')
    ws.set_column('A:A', 20)  
    ws.set_column('B:B', 50)  
    ws.set_column('C:C', 20)  
    ws.set_column('D:D', 10)
    ws.set_column('E:E', 20)
    ws.set_column('F:F', 20)
       
    ws.write(0, 0,'owner')
    ws.write(0, 1,'title')
    ws.write(0, 2,'cla')
    ws.write(0, 3,'look_time')
    ws.write(0, 4,'price')
    ws.write(0, 5,'area')
     
    for i in range(1,36): 
        ws.write(i, 0, '%s' %data[i-1]['owner'])  
    for i in range(1,36): 
        ws.write(i, 1, '%s' %data[i-1]['title'])  
    for i in range(1,36): 
        ws.write(i, 2, '%s' %data[i-1]['cla'])  
    for i in range(1,36): 
        ws.write(i, 3, '%s' %data[i-1]['look_time'])
    for i in range(1,36): 
        ws.write(i, 4, '%s' %data[i-1]['price'])  
    for i in range(1,36): 
        ws.write(i, 5, '%s' %data[i-1]['area'])    
  
    wb.close()  
    
    
url = 'http://sh.58.com/shouji/?PGTID=0d300024-0000-2bc1-11e9-b96cea8ac074&ClickID=1'
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
links = []
hrefs =  get_urls_in_one_page(url,links,headers = headers)

infos = []
for href in hrefs:
    info = get_content(href,headers = headers)
    infos.append(info)
    
path = '~/58.xlsx'

write_xlsx(infos,path)


    
 




