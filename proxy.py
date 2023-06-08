import requests
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import re
from tqdm import tqdm

# create a session object for efficient re-use of the same TCP connection(s)
ses = requests.Session()
ses.cookies = CookieJar()

# function to scrape IP data from a website 
def my_ip_check():
    response = ses.get('https://pr-cy.ru/browser-details/')
    soup = BeautifulSoup(response.text, 'lxml')
    my_ip = soup.find('div',class_='ip-myip').text
    return my_ip

# function to scrape a list of working proxies from a website 
def collect_proxy():
    return
    url = 'https://free-proxy-list.net/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    source = str(requests.get(url, headers=headers, timeout=10).text)
    data = [list(filter(None, i))[0] for i in re.findall('<td class="hm">(.*?)</td>|<td>(.*?)</td>', source)]
    groupings = [dict(zip(['ip', 'port', 'code', 'using_anonymous'], data[i:i+4])) for i in range(0, len(data), 4)]
    final_groupings = [{'full_ip':"{ip}:{port}".format(**i)} for i in groupings]
    if not final_groupings or 1:
        if input('Continue without proxie? (y/n)').lower() != 'y':
            exit()
        else:
            return 
    return final_groupings

# function to check list of proxies for working status and return list of those that are functional 
def prox_ip_check():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36'
    }
    f_proxy = []
    my_ip = my_ip_check()   #obtain current IP address
    proxy = collect_proxy()  #obtain list of working proxies
    if proxy == None:
        return
    for c in tqdm(proxy, desc='Scraping proxies...'):  #loop through proxies
        c = c['full_ip']
        
        session = requests.Session()  #create session object for each proxy
        proxies = { #configure proxy
            'http': f'http://{c}',
            'https': f'https://{c}'
        }
        session.proxies.update(proxies)  #update session settings for configured proxy
        try:
            response_proxy = requests.get('https://pr-cy.ru/browser-details/', headers=headers, timeout=1.5, proxies=proxies)  #make request using proxy
        except:
            continue
        soup_proxy = BeautifulSoup(response_proxy.text, 'lxml')
        fin_ip = soup_proxy.find('div', class_='ip-myip').text  #scrape IP data using proxy
        if fin_ip != my_ip:  #if IP data differs from original IP address, add proxy to final list
            f_proxy.append(proxies)
        
    return f_proxy

if __name__ == "__main__":
    print(prox_ip_check())