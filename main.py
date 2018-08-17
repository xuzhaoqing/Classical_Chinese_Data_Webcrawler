# -*-coding:utf-8 -*-
# Arthur: Zhaoqing Xu

from bs4 import BeautifulSoup
import requests
import re
import os
BASE_URL = 'https://zh.wikisource.org/'
BASE_DIR = os.getcwd() + '\\24Histories\\'

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print('Create Folder ',path)




def get_data():
    with open('24Histories_links.txt','r',encoding='utf-8') as f:
        lines = f.readlines()
        data = []
        for line in lines:
            try:
                link = re.findall('href="(.*)" t', line)[0]
                name = re.findall('title="(.*)"', line)[0]
                data.append((link, name))
            except:
                continue
        return data


def get_chapter_page(c_link,c_name,name):
    path = BASE_DIR + name + '\\' + c_name + '.txt'
    url = BASE_URL + c_link
    r = requests.get(url,allow_redirects = False)
    if(r.status_code == 200):
        soup = BeautifulSoup(r.content,'html.parser')
        p_list = soup.find_all('p')
        string = ''
        for p in p_list:
            string = string + p.text
        with open(path,'w',encoding='utf-8') as f:
            f.write(string)
    else:
        with open('missing.txt', 'a+', encoding='utf-8') as f:
            f.write('URL ' + name+' '+ c_name + ' Got ' + r.status_code + '\n')
        print('URL ', name,c_name,' Got ', r.status_code)


def get_book_page(url,name):
    r = requests.get(url, allow_redirects = False)
    if(r.status_code==200):
        soup = BeautifulSoup(r.content,'html.parser')
        ul_list = soup.find_all('ul')
        for ul in ul_list:
            try:
                title = ul.li.a.get('title')
                if name+'/' in title:
                    for li in ul.find_all('li'):
                            chapter_link = li.a.get('href')
                            chapter_name = li.a.text
                            get_chapter_page(chapter_link,chapter_name,name)
            except:
                continue
    else:
        with open('missing.txt','a+',encoding='utf-8') as f:
            f.write('URL '+name+' Got '+r.status_code+'\n')
        print('URL ', name, ' Got ', r.status_code)

def start(link,name):
    path = BASE_DIR + name + '\\'
    mkdir(path)
    url = BASE_URL+link
    get_book_page(url,name)
    print(name,' has finished')

if __name__ == '__main__':
    data = get_data()
    for link,name in data:
        start(link,name)
