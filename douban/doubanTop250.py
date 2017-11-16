import requests
import xlsxwriter
import re
import urllib
import time
from bs4 import BeautifulSoup

#基于python3

def get_content(url,headers):
    html = requests.get(url,headers).text
    soup = BeautifulSoup(html, 'lxml')

    titles = soup.select('body > div:nth-of-type(3) > div:nth-of-type(1) > div > div.article > ol > li > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a > span:nth-of-type(1)')
    infos = soup.select('ol.grid_view > li > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > p:nth-of-type(1)')    
    briefs = soup.select('ol.grid_view > li > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > p:nth-of-type(2) > span:nth-of-type(1)') 
    scores = soup.select('ol.grid_view > li > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > span:nth-of-type(2)')
    pics = soup.select('ol.grid_view > li > div:nth-of-type(1) > div:nth-of-type(1) > a:nth-of-type(1) > img:nth-of-type(1)')
    
   
   
    
    data = []
    piclist = []
    
    for title,info,score in zip(titles,infos,scores):
        dic = {
            'title':title.get_text(),
            'info':info.get_text().strip(),
            'score':score.get_text(),
            }
        data.append(dic)
    
    
    
    for pic in pics:
        piclist.append(pic.get('src'))
        
        
    return data,piclist,briefs
    
    
def write_xlsx(data,path): 

    wb = xlsxwriter.Workbook(path)
    ws = wb.add_worksheet('豆瓣Top250')
    ws.set_column('A:A', 20)  
    ws.set_column('B:B', 50)  
    ws.set_column('C:C', 60)  
    ws.set_column('D:D', 5)
       
    ws.write(0, 0,'标题')
    ws.write(0, 1,'信息')
    ws.write(0, 2,'简介')
    ws.write(0, 3,'分数')
     
    for i in range(1,251): 
        ws.write(i, 0, '%s' %data[i-1]['title'])  
    for i in range(1,251): 
        ws.write(i, 1, '%s' %data[i-1]['info'])  
    for i in range(1,251): 
        ws.write(i, 2, '%s' %data[i-1]['brief'])  
    for i in range(1,251): 
        ws.write(i, 3, '%s' %data[i-1]['score'])  
  
    wb.close()  
     

if __name__ == '__main__':
    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0' }
    urls = ['https://movie.douban.com/top250?start={}&filter='.format(str(i)) for i in range(0,250,25)] 
    datamul = []
    briefli = []
    for url in urls: 
        time.sleep(2)    
        data,piclist,briefs = get_content(url,headers = headers)
        
        datamul = datamul + data
        briefli = briefli + briefs
        for i in piclist:
            urllib.request.urlretrieve(i,'~/douban/pic/%s'%i[-14:])
            
    #有三部电影没有简介，加入到data时需要跳过 
    j = 0    
    for i in range(1,251):
        if i == 103 or i == 154 or i == 247:
            datamul[i-1]['brief'] = ''
        else:
            datamul[i-1]['brief'] = briefli[j].get_text()
            j += 1
    print (len(datamul))
    path = '~/doubanTop.xlsx'
    write_xlsx(datamul,path)
 

  


  
  
  
  
  
   
   
   





