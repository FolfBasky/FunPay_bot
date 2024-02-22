import requests
from bs4 import BeautifulSoup 
import re
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from data import *
import random
from http.cookiejar import CookieJar
import vk
import time

data_st = {
    'csrf_token':'',
    'g-recaptcha-response':'',
}

def recaptcha(site_key, url):
    api_key = '9202b639f977797ed5b756b0c3af9327'
    client = AnticaptchaClient(api_key)
    task = NoCaptchaTaskProxylessTask(url, site_key)
    try:
        job = client.createTask(task)
    except Exception as e:
        print(e)
        return recaptcha(site_key, url)
    job.join()
    print('captcha_solved')
    return job.get_solution_response()

session = requests.Session()
print(session.get("http://httpbin.org/ip").text)

def validate_ip():
    'check if ip is valid: True if valid, False if not'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.4.776 Yowser/2.5 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'dnt':'1',
    }
    try:
        response = requests.get('https://ip2geolocation.com/', headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
    except Exception as e:
        return False
    if soup.find_all('td', class_='res')[6].text == 'Санкт-Петербург': 
        return False
    else:
        return True 

def logging_():
    if not validate_ip(): return 'Invalid ip!'
    global session, response
    try:
        from sql import get_first_active_account_info
        logging_data = get_first_active_account_info()
        if logging_data is None: return 'No active account!'    
    except:
        return 'Need enter data!'
    
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.4.776 Yowser/2.5 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ru,en;q=0.9',
        #'Connection': 'keep-alive',
        #'Upgrade-Insecure-Requests': '1',
        'dnt':'1',
    }
    session.get('https://funpay.com/')
    session.cookies = CookieJar()
    response = session.get(url='https://funpay.com/account/login', headers=headers)
    if response.status_code != 200: return 'Bad internet connection!'
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = re.search(r'csrf_token.{0,}=.{0,}"',response.text)[0].split()[1][7:-1]
    data_st['csrf_token'] = csrf_token
    site_key = soup.find_all('div', class_='g-recaptcha')[0]['data-sitekey']
    data_st['g-recaptcha-response'] = recaptcha(site_key, url='https://funpay.com/account/login')
    data_st['login'] = logging_data['login']
    data_st['password'] = logging_data['password']
    try:
        response = session.post('https://funpay.com/account/login', data=data_st, headers=headers)
    except:
        print('Fail use proxy')
        return 'Fail use proxy'
    if response.status_code != 200 or 'Войти' in response.text: 
        error_msg = BeautifulSoup(response.text,'lxml').find('ul',class_='form-messages text-danger').text.strip()
        print(error_msg)
        return error_msg
    

    headers1 = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ru,en;q=0.9',
        'content-length': '23',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://funpay.com',
        'referer': 'https://funpay.com/security/ipChallenge',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'authority': 'funpay.com',
        'method': 'POST',
        'path': '/security/ipChallengeCheck',
        'scheme': 'https'
    }
    print( set_valute() )
    response = session.get(url='https://funpay.com/security/ipChallenge')
    if response.text.lower().find('телефон') != -1: 
        lg = logging_data['phone_number'][-4:]
    elif response.text.lower().find('карта') != -1:
        lg = logging_data['card_number'][-4:]
    else:
        if 'Страница не найдена' in response.text:
            return
        else: 
            return 'Fail last num!'
    data = {
        '0': lg,
        '1': lg,
        'csrf_token':'undefined'
    }
    response = session.post(url='https://funpay.com/security/ipChallengeCheck', data=data, headers=headers1)
    if response.status_code != 200:
        print('Fail last num')
        return 'Fail last num'
        

def set_valute():
    response = session.get('https://funpay.com/en/lots/699/?setlocale=ru')
    data = {
        'cy': 'rub',
        'csrf_token': data_st['csrf_token'],
        'confirmed': 'true'
    }
    headers = {
        'accept': '*/*',
        'content-type': 'text/plain;charset=UTF-8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.3.949 Yowser/2.5 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        }
    response = session.post('https://funpay.com/account/switchCurrency', data=data, headers=headers)
    try:
        if response.json()['url'] == '': return 'Swith was succesfull'
        else: return response.json()
    except:
        return 'Switch was fail'


def collect_chats():
    'username, last_msg, link'
    response = session.get(url='https://funpay.com/chat/')
    soup = BeautifulSoup(response.text, 'lxml')
    result = []
    try:
        count = int(soup.find('span', {'class':['badge badge-chat hidden','badge badge-chat']}).text.strip().replace('\n', ''))
        if count < 3: count = 3
    except:
        count = 3
    # all_messages_count = len(soup.find_all('a', class_='contact-item'))
    try:
        for x in range(count):
            last_msg = ' '.join(soup.find_all('a', class_='contact-item')[x].text.strip().replace('\n', ' ').split()[1:])
            link = soup.find_all('a', class_='contact-item')[x]['href'].strip().replace('\n', ' ')
            username = soup.find_all('a', class_='contact-item')[x].contents[3].text.strip().replace('\n', ' ')
            result.append([username, last_msg, link])
    except:
        pass
    return result

def check_messages(url):
    response = session.get(url)
    if response.text.find('Здесь пока ничего нет ¯\\_(ツ)_/¯') != -1:
        return 'Fail'
    soup = BeautifulSoup(response.text, 'lxml')
    all_message = []
    messages = soup.find_all('div', class_='chat-message')
    online = soup.find('div', class_='media-user-status').text
    all_message.append(online)
    for x in messages:
        try:
            try:
                text = x.contents[1::2][1].text.strip()
                date = x.contents[1::2][0].contents[-2].attrs['title']
                username = x.contents[1::2][0].text.strip().split()[0]
            except:
                text = x.contents[1::2][0].text.strip()
            
            all_message.append(f'{username} ({date})')
            all_message.append(text)
        except:
            pass

    return '\n'.join(all_message)

def message_answer_r(url, text, V=1):
    text = text.replace('\n', ' ')
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = soup.find('body',class_='bg-light-color')['data-app-data'].split(',')[1].split(':')[1].replace('"', '')
    data_orders = soup.find_all('div',class_='hidden')[2]['data-orders']
    data_id_cpu = soup.find('div',{'class':['param-item chat-panel hidden', 'param-item chat-panel']})['data-id']
    data_tag_cpu = soup.find('div',{'class':['param-item chat-panel hidden', 'param-item chat-panel']})['data-tag']
    last_message_id = soup.find_all('div', class_='chat-msg-item')[-1].attrs['id'].split('-')[1]
    data_tag = soup.find_all('div', class_='chat chat-float')[0]['data-tag']
    data_user = soup.find_all('div', class_='chat chat-float')[0]['data-user']
    data_tag_book = soup.find_all('div', class_='chat chat-float')[0]['data-bookmarks-tag']
    if V == 1: data_node_book = f'users-{data_user}-{data_id_cpu}'
    else: data_node_book = f'users-{data_id_cpu}-{data_user}'
    data = {
        'objects': '[{{"type":"orders_counters","id":"{}","tag":"{}","data":false}},{{"type":"chat_node","id":"{}","tag":"{}","data":{{"node":"{}","last_message":{},"content":"{}"}},{{"type":"chat_bookmarks","id":"{}","tag":"{}","data":false}},{{"type":"c-p-u","id":"{}","tag":"{}","data":false}}]'.format(data_user, data_orders, data_node_book, data_tag, data_node_book, last_message_id, text, data_user, data_tag_book, data_id_cpu, data_tag_cpu),
        'request': '{{"action":"chat_message","data":{{"node":"{}","last_message":{},"content":"{}" }}}}'.format(data_node_book, last_message_id, text),
        'csrf_token': csrf_token
    }
   
    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    response = session.post(url='https://funpay.com/runner/', data=data, headers=headers)
    if response.json()['response']['error'] == None: return 'Message was sended'
    else: 
        if V == 2: return response.json()['response']['error']
        return message_answer_r(url,text,V=2)
 
def create_lot(personally_token,groups_data,deleted = "", offer_id:str = '0'):
    ds_list = [['☑️ VK СООБЩЕСТВО - 🔥🌩️ СООБЩЕСТВО ДЛЯ СТАРТА (',' ПОДПИСЧИКОВ) 🔥🌩️ БЫСТРО 🔥🌩️ ГАРАНТИЯ 100%☑️']]
    #['🔥Живой паблик','подписчиков 🔥СООБЩЕСТВО ДЛЯ СТАРТА🔥БЕЗ БЛОКИРОВКИ 🔥'],
    #['Вк группа под смену тематики/ высшее качество 🔥', 'подписчиков']]
    describe = random.choice(ds_list)
    with open('data.py','r') as e:
        kef = e.readlines()[0].strip().split()[2]
        kef = float(kef)

    for el in groups_data.items():
        url,subs = el
        try:
            screen_name = requests.get('https://api.vk.com/method/groups.getById?',
                params = {
                'group_id' : url,
                'access_token': personally_token,
                'v': vk.version
                }
            ,timeout=10).json()['response'][0]['screen_name']     
        except:
            screen_name = url   
        
        headers1 = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
        }

        data = {
            "csrf_token": data_st['csrf_token'],
            'form_created_at':	time.time(),
            "offer_id": offer_id,
            "node_id": "699",
            "deleted": deleted,
            'location':	"",
            "fields[subject]": "Блогеры" if deleted == "" else "",
            "fields[followers]": subs if deleted == "" else "",
            "fields[summary][ru]": f'{describe[0]} {str(subs)} {describe[1]}' if deleted == "" else "",
            "fields[summary][en]": "",
            "fields[desc][ru]":'Передаю права владельца. Ссылка на группу: https://vk.com/'+ screen_name,
            "fields[desc][en]": "",
            'fields[payment_msg][ru]':	"",
            'fields[payment_msg][en]':	"",
            'secrets':"",
            'amount':"1",
            "price": str(round(int(subs)/10 * kef)) if deleted == "" else "",
            "active": "off" if deleted == "" else "on", 
        }

        response = session.post(url='https://funpay.com/lots/offerSave',data=data, headers=headers1)
        if response.status_code != 200 and 'done' not in response.text[:50]:
            return 'Fail'
        time.sleep(3)
        
    return 'Slots was created!'

def up_lots():
    data = {
        'game_id': '221',
        'node_id': '699'
    }

    headers2 = {
        "authority": "funpay.com",
        "method": "POST",
        "path": "/lots/raise",
        "scheme": "https",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "ru,en;q=0.9",
        "content-length": "23",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "dnt": "1",
        "origin": "https://funpay.com",
        "referer": "https://funpay.com/lots/699/trade",
        "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Yandex\";v=\"23\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    response = session.post(url='https://funpay.com/lots/raise', data=data, headers=headers2)
    try:
        return response.json()['url']
    except:
        pass
    if response.status_code != 200:
        return 'Fail'
    if '"error":1' in response.text.split(',')[1]:
        return(response.text.split(',')[0].split(':')[1][1:-1])
    else:
        return('Slots was upped!')

def delete_slots():
    response = session.get(url='https://funpay.com/lots/699/trade')
    soup = BeautifulSoup(response.text, 'lxml')
    all_lots = {}
    for x in soup.find_all('a', class_='tc-item'):
        all_lots[x['data-offer']] = x.text
    
    for x in all_lots.keys():
        headers1 = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
        }

        data = {
            "csrf_token": data_st['csrf_token'],
            'form_created_at':	time.time(),
            "offer_id": x,
            "node_id": "699",
            "deleted": '1',
            'location':	"",
            "fields[subject]": "Блогеры",
            "fields[followers]": "",
            "fields[summary][ru]": "",
            "fields[summary][en]": "",
            "fields[desc][ru]":'',
            "fields[desc][en]": "",
            'fields[payment_msg][ru]':	"",
            'fields[payment_msg][en]':	"",
            'secrets':"",
            'amount':"1",
            "price": '',
            "active": "off", 
        }
        response = session.post(url='https://funpay.com/lots/offerSave',data=data, headers=headers1)
        if response.status_code != 200:
            return 'Fail'
    return 'Slots was delete'
    

def withdrow_money(wallet=0):
    response = session.get('https://funpay.com/account/balance')
    soup = BeautifulSoup(response.text, 'lxml')
    balance = soup.find_all(class_="page-header balances-header page-header-no-hr")[0].text.strip()
    balance_val = re.search(r'\d{0,} ₽', balance)[0].split()[0]
    data = {
        "csrf_token": data_st['csrf_token'],
        "preview": "",
        "currency_id": "rub",
        "ext_currency_id": "card_rub",
        "wallet": str(wallet),
        "amount_int": str(balance_val)
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ru,en;q=0.9',
        'content-length': '117',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36',
        'Origin':'https://funpay.com',
        'Referer': 'https://funpay.com/account/balance',
        'X-Requested-With':'XMLHttpRequest',
    }
    response = session.post(url='https://funpay.com/withdraw/withdraw',data=data, headers=headers)
    try:
        return response.json()['msg']
    except:
        return 'Money was sended!'

def check_balance_operation():
    response = session.get('https://funpay.com/account/balance')
    soup = BeautifulSoup(response.text, 'lxml')
    operations = soup.find_all('div', {'class':['tc-item transaction-status-complete','tc-item transaction-status-cancel','tc-item transaction-status-waiting']})
    return [x.text + '\n' + x['data-transaction'] for x in operations][:10]

def check_orders_or_sales(sales=True):
    url = 'https://funpay.com/orders/' + ('trade' if sales else '')
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    order_tag = soup.find_all('div',class_='tc-order')
    order_status = soup.find_all('div',{'class':['tc-status text-success', 'tc-status text-warning', 'tc-status text-waiting', 'tc-status text-primary']})
    user_info = soup.find_all('span',class_='pseudo-a')
    date = soup.find_all('div', class_='tc-date-time')
    price = soup.find_all('div',{'class':['tc-price text-nowrap tc-seller-sum','tc-price text-nowrap tc-buyer-sum']})
    result = []
    for x in range(len(order_tag)):
        result.append([order_status[x].text, order_tag[x].text, user_info[x].contents[0], user_info[x]['data-href'], date[x].text, price[x].text])
    return result

def check_sale(tag):
    tag = tag.replace('#','')

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.4.776 Yowser/2.5 Safari/537.36'
    }

    response = session.get(f'https://funpay.com/orders/{tag}/', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    desc = soup.find_all('div', class_='param-item')[5].text
    link = re.search(r'https.{0,}\n',desc)[0][:-1]
    return desc, link

def check_lots_r():
    response = session.get(url='https://funpay.com/lots/699/trade')
    soup = BeautifulSoup(response.text, 'lxml')
    all_lots = {}
    for x in soup.find_all('a', class_='tc-item'):
        all_lots[x['data-offer']] = x.text
    return all_lots

def edit_lot_r(offer_id, deleted = '1', followers = '', summary = '', desc = '', price = ''):
    headers1 = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
        }

    data = {
            "csrf_token": data_st['csrf_token'],
            "offer_id": offer_id,
            "node_id": "699",
            "deleted": deleted,
            "fields[subject]": "Магазины",
            "fields[followers]": followers,
            "fields[summary][ru]": summary,
            "fields[summary][en]": "",
            "fields[desc][ru]": desc,
            "fields[desc][en]": "",
            "price": price,
            "active": "on", 
            "deactivate_after_sale[]": "on",
            "location": "trade"
        }
    response = session.post(url='https://funpay.com/lots/offerSave',data=data, headers=headers1)
    if response.status_code == 200 and response.json()['done']:
        return 'Succesfull'
    else:
        return 'Fail'

def complete_order(tag):
    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With':'XMLHttpRequest',
    }
    data = {
        'csrf_token': data_st['csrf_token'],
        'id':tag.replace('#','')
    }
    response = session.post('https://funpay.com/orders/complete', data=data, headers=headers)
    return response.json()['msg']

def refund_order(tag):
    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With':'XMLHttpRequest',
    }
    data = {
        'csrf_token': data_st['csrf_token'],
        'id':tag.replace('#','')
    }
    response = session.post('https://funpay.com/orders/refund', data=data, headers=headers)
    return response.json()

def cancel_balance_operation(id):
    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With':'XMLHttpRequest',
    }
    data = {
        'csrf_token': data_st['csrf_token'],
        'id': id,
        'action': 'cancel'
    }
    response = session.post('https://funpay.com/users/transactionAction', data=data, headers=headers)
    return response.json()['msg']

def get_balance_r():
    response = session.get('https://funpay.com/account/balance')
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        balance = soup.find(class_="page-header balances-header").text.strip()
    except:
        balance = soup.find(class_="page-header balances-header page-header-no-hr").text.strip()
    return balance

def check_feedback():
    response = session.get('https://funpay.com/')
    soup = BeautifulSoup(response.text, 'lxml')
    main_link = soup.find('a',class_='user-link-dropdown')['href']
    response = session.get(main_link)
    soup = BeautifulSoup(response.text, 'lxml')
    result = []
    for x in range(len(soup.find_all('div', class_='review-item-rating pull-right hidden-xs'))):
        stars = soup.find_all('div', class_='review-item-rating pull-right hidden-xs')[x].contents[0].contents[0]['class'][0]
        text = soup.find_all('div', class_='review-item-text')[x].text.strip()
        detail = soup.find_all('div', class_='review-item-detail')[x].text
        date = soup.find_all('div', class_='review-item-date')[x].text
        order = soup.find_all('div', class_='review-item-order')[x].contents[0].text
        result.append((order, date, detail, text, stars))
    return result

def get_nickname():
    response = session.get('https://funpay.com/')
    soup = BeautifulSoup(response.text,'lxml')
    return soup.find('div', class_='user-link-name').text

def logout():
    global session
    response = session.get('https://funpay.com/')
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        for el in soup.find_all('li'):
            if el.text == 'Выйти': 
                url = el.next['href']
                break
        response = session.get(url)
        session = requests.Session()
        return [True]
    except Exception as e:
        return [False, e]

def change_account(login = 'jerk37673@gmail.com', active = 1):
    from sql import set_active_status_accounts, set_account_active, get_first_active_account_info
    set_active_status_accounts()
    set_account_active(login, active)
    print(get_first_active_account_info())

def register_account(nickname, email, password):
    'register account, return True if success'
    response = session.get(url:='https://funpay.com/account/register')
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = re.search(r'csrf_token.{0,}=.{0,}"',response.text)[0].split()[1][7:-1]
    site_key = soup.find_all('div', class_='g-recaptcha')[0]['data-sitekey']
    
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.696 Yowser/2.5 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        }

    data = {
        'csrf_token':csrf_token,
        'name':nickname,
        'email':email,
        'password':password,
        'agreement': 'on',
        'g-recaptcha-response':recaptcha(site_key, url=url),
        #'captchaHidden': '1'
        }
    
    response = session.post('https://funpay.com/account/registerAction', data=data, headers=headers)
    try:
        if response.json()['errors'] == []: return True
        else: 
            print(response.json()['errors'])
            return False
    except Exception as e:
        print(e)
    

def activate_account(url):
    'after register account, you get a link on your email'
    if url == '': return
    session.get(url)

def pass_the_test(phone) -> bool:
    '''when the account is just activatet, you need to pass the test
    #? return False if all was success '''

    try:
        logging_()
    except:
        pass
    global headers
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.696 Yowser/2.5 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        }

    data = {
        'accept':'1',
        }

    response = session.post('https://funpay.com/trade/acceptRules', data=data, headers=headers)

    response = session.post(url:='https://funpay.com/account/phone')
    soup = BeautifulSoup(response.text, 'lxml')
    site_key = soup.find_all('div', class_='g-recaptcha')[0]['data-sitekey']
    csrf_token = re.search(r'csrf_token.{0,}=.{0,}"',response.text)[0].split()[1][7:-1]

    global data_n
    data_n = {
        'csrf_token': csrf_token,
        'mode': 'phone',
        'phone': phone,
        'g-recaptcha-response': recaptcha(site_key, url=url),
        'code':'' 
        }

    response = session.post('https://funpay.com/account/phoneVerification',data=data_n, headers=headers)

    if response.json()['error']:return True
    else: return False

def pass_the_test_code(code):
    'enter code to confirm phone'
    global data_n, headers
    try:
        data_n['mode'] = 'code'
        data_n['code'] = code
        response = session.get(url:='https://funpay.com/account/phone')
        soup = BeautifulSoup(response.text, 'lxml')
        site_key = soup.find_all('div', class_='g-recaptcha')[0]['data-sitekey']
        data_n['g-recaptcha-response'] = recaptcha(site_key, url=url)
        response = session.post('https://funpay.com/account/phoneVerification',data=data_n, headers=headers)
    except:
        pass
    
    if response.json()['error']: return True
    else: return response.json()['error']

def main():


    from tg_new import generate_random_string
    if not register_account(nickname=generate_random_string(3),email=(email:='farafara21212@gmail.com'), password=(password:=generate_random_string(4))):
        print('Fail')
        return
    print(f'{password=}')
    url = input('Enter url: ')
    activate_account(url)
    phone = '89311182608'

    from sql import add_user_profile
    add_user_profile(1,email,password,phone)
    change_account(email)
    print(pass_the_test(phone))
    print(pass_the_test_code(input('Enter code: ')))
    '''change_account()
    print(logging_())
    print(logout())'''
    #collect_chats()
    #print(get_nickname())
    #print(check_messages(collect_chats()[0][2]))
    #print(check_sale('#GYPLRXRJ'))
    ...



if __name__ == '__main__':
    #validate_ip()
    main()
