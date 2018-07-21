import json
import re
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0"}

def get_one_page(url):
    '''
    爬取网页
    :param url:
    :return:
    '''
    try:
        response=requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    '''
    解析网页
    :param html:
    :return:
    '''
    pattern = re.compile('<li>.*?<em class="">(\d+)</em>.*?info">.*?title">(.*?)</span>.*?<p class="">.*?导演:(.*?)&nbsp;&nbsp;&nbsp;(.*?)<br>.*?(\d+)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)\n.*?</p>.*?<span class="rating_num" property="v:average">(.*?)</span>.*?content="10.0"></span>.*?<span>(\d+)人评价</span>.*?</div>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index':item[0],
            'title':item[1],
            'director':item[2],
            'actor':item[3],
            'release_time':item[4],
            'location':item[5],
            'label':item[6],
            'score':item[7],
            'users':item[8]
        }

def write_to_file(content):
    '''
    保存文件
    :param content:
    :return:
    '''
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.close()

def main(start):
    url='https://movie.douban.com/top250?start='+str(start)+'&filter='
    html=get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
if __name__ == '__main__':
    for i in range(10):
        main(i*25)
    # pool = Pool()
    # pool.map(main,[i*25 for i in range(10)])
    # pool.close()
    # pool.join()