JHTYP
O0IU E80N YUEGCKSJNB/LKGNKUHRG;VUSEGLUYCBSDL,JHVB/SDBV/ABHVAEUGHEVUGVBUEBCFHDGHGJHBLDSJB.UEGLESUGFBVKDJXBFGUIRBV import requests
from bs4 import BeautifulSoup 
import re
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask

url = 'https://funpay.com/account/login'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'cookie': '_ym_uid=1664392478761396691; _ym_d=1664392478; _ga=GA1.2.1248129166.1664392478; _gid=GA1.2.1662993909.1676899345; _ym_isad=1; PHPSESSID=p4GzG1%2C583O7lL9%2CfTFDoGSoJ30ldvUe',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36'
    }

data_st = {
    'csrf_token':'',
    'login':'Aytan',
    'password':'4870535a',
    'g-recaptcha-response':'',
}Z

def recaptcha(site_key, url):
    api_key = '9202b639f977797ed5b756b0c3af9327'
    client = AnticaptchaClient(api_key)
    task = NoCaptchaTaskProxylessTask(url, site_key)
    job = client.createTask(task)
    job.join()
    return job.get_solution_response()

session = requests.Session()

response = session.get(url, headers=headers)
headers['cookie'] = ';'.join(headers['cookie'].split(';')[:-1]) + '; PHPSESSID=' + session.cookies.get_dict()['PHPSESSID']
soup = BeautifulSoup(response.text, 'lxml')
site_key = soup.find_all('div', class_='g-recaptcha')[0]['data-sitekey']
csrf_token = re.search(r'csrf_token.{0,}=.{0,}"',response.text)[0].split()[1][7:-1]
data_st['g-recaptcha-response'] = recaptcha(site_key, url)
data_st['csrf_token'] = csrf_token



response = session.post(url, data_st, headers)
1