import asyncio
import os
import sqlite3
import pyautogui as root
import time 
import pyperclip 
from aiogram import Bot, Dispatcher, executor, types
import logging
import requests
import random
import string
import psutil 
import keyboard as keyboard_button
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
from PIL import Image, ImageDraw, ImageFont


def captcha_solved():
    api_key = '9202b639f977797ed5b756b0c3af9327'
    captcha_fp = open('captcha_ms.jpeg', 'rb')
    client = AnticaptchaClient(api_key)
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task)
    job.join()
    print('Captcha key = ',job.get_captcha_text())
    return (job.get_captcha_text())

personally_token = 'vk1.a.AvuIMTICUJN18VjUmAzfVHLkYEmAApgBFdlMRebLUU-455OpG3d_3aO588NHKkM5W0RuQ4C3LjmWgPSxheTL2jAX_xR9mE6gIZpkfbnmAsrN-tdyGkCW7acbNA0D04lKjFAT3YHHmmLwSAEimkSbVHv3hfLhIO44lFOTcIn4EpfuETRfSziQ8QXeyIobEF8x-VWKDedyS2EaPP8Vl6L57Q'
vk_token = '954a0da6954a0da6954a0da652965a41679954a954a0da6f7bfbfaf7ac089158dc4976e'
user_id = 339721894
version = '5.131'

bot = Bot(token="5571779165:AAFC8iMTKtS3PHR65IxIEqaB8R7KmbdN_YE")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["/check_message","/create_slots","/delete_slots","/clear_groups", "/up", "/post"]
keyboard.add('/start_tor','/close_tor',*buttons,"/auto")

root.FAILSAFE = False
not_check = {}

x1,x2 = (0,0)#(110,50)
class Desktop(object):
    home = (1365,767)
    tor = (714,767)
    windows = (108,767)
    last_window = (373,203)
    turn_tor = (1140+x1,63-x2)
    close_Tor = (1232+x1, 64-x2)
c1,c2 = (0,0)#(85, 70)
class Tor(object):
    funpay = 'https://funpay.com'
    profile_link = "https://funpay.com/lots/699/trade"
    chat_link = "https://funpay.com/chat/"
    link_coordinates = (580-c1,116-c2)
    button_coordinates = (950-c1,242-c2) 
    chat_new = (450-c1,300-c2)
    window_coordinates_high = (515-c1,286-c2)
    window_coordinates_low = (966-c1,644-c2)
    nick_start = (590-c1,235-c2)
    nick_end = (750-c1,235-c2)
    chat_write_coordinates = (650-c1, 679-c2)
    enter = (800-c1, 188-c2)
    login = 'shalof'
    password = 'Beaos540'
    login_coordinates = (600-c1,492-c2)
    password_coordinates = (600-c1,529-c2)
    number_coordinates = (742-c1, 300-c2)
    number = '7266'
    class slots:
        link = 'https://funpay.com/lots/699/trade'
        create = (600, 330)
        create_again = (1157-c1,229-c2)
        subscribers_coordinates = (695-c1, 373-c2+20)
        subscribers = int()
        themes_coordinates = (686-c1, 287-c2+30)
        smallDiscribe_coordinates = (670-c1, 500)
        ds_list = [['❤💛🧡💚💙💜 ПЕРЕДАЧА ПРАВ ВЛАДЕЛЬЦА ГРУППЫ |', 'ПОДПИСЧИКОВ ❤💛🧡💚💙💜'],['🈴🈵🈲🈴🈵🈲 ПЕРЕДАЮ ПРАВА ВЛАДЕЛЬЦА |','УЧАСТНИКОВ 🈴🈵🈲🈴🈵🈲'], ['🈶🈚🈸🈺🈶🈚 ПЕРЕДАЧА ПРАВ НА УПРАВЛЕНИЕ |','ПОДПИСЧИКОВ 🈶🈚🈶🈚🈸🈺']]
        Des_list = random.choice(ds_list)
        smallDiscribe_text = ''
        Discribe_coordinates = (640-c1, 606-c2+30)
        Discribe_text = 'ПЕРЕДАЮ ПРАВА ВЛАДЕЛЬЦА\n'
        price_coordinates = (545,514)
        price = str()
        save = (585-c1,672-c2+30)
        slot = (633-c1, 332-c2+30)
        delete = (750,640)
        confirm_delete = (750,600)


    class vk:
        a = open('groups.txt','r')
        groups = (a.read()).split('\n')
        a.close()
        groups.pop(-1)

def generate_random_string(lenght):
    vowels = consonants = []
    vowels = [x for x in list(string.ascii_lowercase) if x in 'aeiouy']
    consonants = [x for x in list(string.ascii_lowercase) if x not in 'aeiouy']

    result = ''
    for i in range(3):
        result += random.choice(consonants)
        result += random.choice(vowels)
    else:
        for i in range(2): result += random.choice(list(string.digits))

    return result.capitalize()
names = []
for i in range(200):
    names.append(generate_random_string(3))


#START_BD#
########################################################
def creating():# Создание таблицы
    with sqlite3.connect('messages_base.db') as db:
        c = db.cursor()
        try:
            c.execute("""CREATE TABLE messages_base (
                nickname text,
                last_text text,
                link text
            )""")
        except Exception as error:
            return (error)

def adding(nickname = str, last_text = str, link = str):# Добавление данных
    with sqlite3.connect('messages_base.db') as db:
        c = db.cursor()
        try:
            c.execute(f"INSERT INTO messages_base VALUES ('{nickname}', '{last_text}', '{link}')")
        finally:
            db.commit()

def delete(nickname = None, last_text = None, link = None): # Удаление данных
    if nickname != None: name = 'nickname'; value = nickname
    elif last_text != None: name = 'last_text'; value = last_text
    elif link != None: link = 'nickname'; value = link

    with sqlite3.connect('messages_base.db') as db:
        c = db.cursor()
        try:
            c.execute(f"DELETE FROM messages_base WHERE {name} = '{value}'")
        finally:
            db.commit()

def change(new_text, nickname = str):# Изменение данных
    with sqlite3.connect('messages_base.db') as db:
        c = db.cursor()
        try:
            c.execute(f"UPDATE messages_base SET last_text = '{new_text}' WHERE nickname = '{nickname}'")
        except Exception as e:
            print(e)
        finally:
            db.commit()

def selecting(nickname = None, last_text = None, link = None): # Выборка данных
    if nickname != None: name = 'nickname'; value = nickname
    elif last_text != None: name = 'last_text'; value = last_text
    elif link != None: link = 'nickname'; value = link

    with sqlite3.connect('messages_base.db') as db:
        c = db.cursor()
        try:
            c.execute(f"SELECT * FROM messages_base WHERE {name} = '{value}'")
            #return c.fetchall()
            #print(items)
            #print(c.fetchmany(1))
            return (c.fetchone())
        except Exception as error:
            return (error)

def check_all():
    with sqlite3.connect('messages_base.db') as db:
        c = db.cursor()
        try:
            c.execute("SELECT * FROM messages_base")
            return ( c.fetchall())
            #print(items)
            #print(c.fetchmany(1))
            #print(c.fetchone())
        except Exception as error:
            return ((error))

#END_BD#
########################################################

def click(s,k=1): # s = x,y , k = amount of clicks
    x,y = s
    root.click(x,y,clicks = k)

def write(s,text): # s = x,y , text = your text
    x,y = s
    root.click(x,y)
    time.sleep(1.5)
    root.write(text)
    root.press("enter")

def paste(s,text,enter = True): # s = x,y , text = your text
    x,y = s
    pyperclip.copy(text)
    root.click(x,y,3)
    time.sleep(0.5)
    keyboard_button.press_and_release('ctrl+v')
    if enter == True: keyboard_button.press_and_release('enter')

def start_tor():
    click(Desktop.tor,2)
    time.sleep(100)
    paste(Tor.link_coordinates,Tor.funpay)
    time.sleep(2)
    click(Tor.enter)
    time.sleep(10)
    paste(Tor.login_coordinates,Tor.login,False)
    time.sleep(0.15)
    click(Tor.login_coordinates)
    time.sleep(1.5)
    paste(Tor.password_coordinates,Tor.password, False)
    time.sleep(100) # Captcha 
    paste(Tor.number_coordinates,Tor.number)
    time.sleep(5)
    click(Desktop.turn_tor)
    return 'Enter was done' 

def auto_up(): 
    time.sleep(2)
    click(Desktop.tor,2)
    time.sleep(10)
    paste(Tor.link_coordinates,Tor.profile_link)
    time.sleep(7)
    click(Tor.button_coordinates,2)
    time.sleep(1.5)
    click(Desktop.turn_tor)
    return 'Was done!'

def message_checker(scroll = 0): 
    if scroll <= 1:
        click(Desktop.tor,2)
        time.sleep(1)
        paste(Tor.link_coordinates,Tor.chat_link)
    
    time.sleep(2.75)
    root.moveTo(Tor.chat_new)
    
    if scroll != 0 : time.sleep(1)
    root.move(0,63*scroll)
    if scroll != 0 : time.sleep(1)
    root.click()
    time.sleep(5)
    
    root.moveTo(Tor.nick_start)
    root.dragTo(Tor.nick_end, duration=0.3, button='left')
    root.hotkey('ctrl','c')
    time.sleep(0.5)
    nick = pyperclip.paste()
    time.sleep(1)

    root.moveTo(Tor.window_coordinates_high)
    root.dragTo(Tor.window_coordinates_low, duration=0.5, button='left')
    root.hotkey('ctrl','c')
    time.sleep(0.5)
    text = pyperclip.paste()

    root.click(Tor.link_coordinates)
    time.sleep(1)
    root.hotkey('ctrl','c')
    time.sleep(0.5)
    link = pyperclip.paste()

    if scroll == 0 or scroll == 4: click(Desktop.turn_tor)

    text = text.replace('\r\n',' ')
    """
    for months in range(1,13):
        for days in range(1,32):
            times = (f'{str(days).rjust(2,"0")}.{str(months).rjust(2,"0")}.{str(round(time.time() / 31536000) + 1969)[-1:-2]}')
            text = text.replace(times,'')"""

    for hours in range(24):
        for minutes in range(60):
            for secundes in range(60):
                times = (f'{str(hours).rjust(2,"0")}:{str(minutes).rjust(2,"0")}:{str(secundes).rjust(2,"0")}')
                text = text.replace(times,'')
     
    while text.find('FunPay оповещение') != -1:
        funpay_order = [text.find('FunPay оповещение')-1,text.find(".",text.find('FunPay оповещение'))+1]
        funpay_order_text = text[funpay_order[0]:funpay_order[1]]
        if f'{nick} оплатил заказ ' in funpay_order_text:
            return (link,f'Найден покупатель, оплативший заказ. \n{"#"*20}',text)
        elif f'{Tor.login} оплатил заказ ' in funpay_order_text:
            funpay_order = [text.find('FunPay оповещение')-1,text.find("».",text.find('FunPay оповещение'))+2]
            funpay_order_text = text[funpay_order[0]+  +funpay_order[1]]
        text = text[:funpay_order[0]] + ' *операции на сайте* ' + text[funpay_order[1]:]
        time.sleep(0.05)
    return (nick[2:],text,link)

def messages_answer(link,text1): #text = text that bot send user
    time.sleep(2)
    click(Desktop.tor,2)
    time.sleep(1)
    paste(Tor.link_coordinates,link)
    time.sleep(2)
    if link == Tor.chat_link:
        click(Tor.chat_new)
        time.sleep(1.5)
    paste(Tor.chat_write_coordinates,text1)
    time.sleep(0.5)
    click(Desktop.turn_tor)
    return "Was done!"

def create_slots():
    
    

    def paste1(s,text,k = True): # s = x,y , text = your text
        x,y = s
        root.click(x,y,3)
        time.sleep(0.05)
        pyperclip.copy(text)
        time.sleep(0.05)
        keyboard_button.press_and_release('ctrl+v' )
        if k == True: keyboard_button.press_and_release('enter')


    time.sleep(2)
    click(Desktop.tor,2)
    time.sleep(2)
    paste(Tor.link_coordinates,Tor.slots.link)
    time.sleep(10)
    click(Tor.slots.create)
    time.sleep(7)
    subscribers = []
    link = []
    prices = 0
    for k,i in enumerate(Tor.vk.groups):

        screen_name = requests.get('https://api.vk.com/method/groups.getById?',
        params = {
        'group_id' : i.split(':')[0],
        'access_token': personally_token,
        'v': version
        }
        ).json()['response'][0]['screen_name']

        if k != 0:
            #paste(Tor.link_coordinates,Tor.slots.link)
            #time.sleep(2)
            click(Tor.slots.create_again)
            time.sleep(7)   
        subscribers.append(i.split(':')[1])
        link.append( i.split(':')[0])
        click(Tor.slots.themes_coordinates)
        time.sleep(0.25)
        click((647, 359))
        time.sleep(0.25)
        
        paste1(Tor.slots.subscribers_coordinates,subscribers[k],False)
        root.click()
        time.sleep(0.25)
        paste1(Tor.slots.smallDiscribe_coordinates,f'{Tor.slots.Des_list[0]} {str(subscribers[k])} {Tor.slots.Des_list[1]}',False)
        root.click()
        time.sleep(0.3)
        paste1(Tor.slots.Discribe_coordinates,Tor.slots.Discribe_text + 'https://vk.com/'+ screen_name + '\nСамая низкая цена на рынке!\nПередаю быстро\nПрава владельца группы',False)
        root.click()
        time.sleep(0.25)
        root.scroll(-1000)
        time.sleep(0.25)
        prices += round(int(subscribers[k])/10 * kef)
        paste1(Tor.slots.price_coordinates,str(round(int(subscribers[k])/10 * kef)))
        root.click()
        time.sleep(7)
        k += 1
    click(Desktop.turn_tor)
    return 'All slots was created!\nAbout ' + str(prices) + ' rub profit'

def delete_slots():
    time.sleep(2)
    click(Desktop.tor,2)
    time.sleep(2)
    paste(Tor.link_coordinates,Tor.slots.link)
    time.sleep(5)

    for i in Tor.vk.groups:
        click(Tor.slots.slot)
        time.sleep(2)
        root.scroll(-10000)
        time.sleep(0.3)
        click(Tor.slots.delete)
        time.sleep(0.3)
        click(Tor.slots.confirm_delete)
        time.sleep(1.5)
    else:
        click(Desktop.turn_tor)
    return 'All slots was deleted!'

def get_admins_groups():
    response = requests.get('https://api.vk.com/method/groups.get?',
        params = {
        'user_id' : user_id,
        'extended' : 0,
        'filter' : 'admin',
        'access_token': personally_token,
        'v': version
        }
        )
    return (response.json()['response']['items'])

def count_subscribers(link):
    response = requests.get('https://api.vk.com/method/groups.getMembers?',
        params = {
        'group_id' : link,
        'access_token': personally_token,
        'v': version
        }


        
        )
    try:
        count_sub = (response.json()['response']['count'])
        if count_sub > 500 and count_sub < 100000: return(count_sub)
    except:
        pass

def groups():
    admins_groups = get_admins_groups()
    grops_count_subscribers = []
    for i in admins_groups:
        grops_count_subscribers.append(count_subscribers(i))
    groups = dict(zip(admins_groups,grops_count_subscribers))
    groups = {i: j for i, j in groups.items() if j!=None }
    with open('groups.txt','w') as a:
        group_link,group_subscribers = list(groups.keys()),list(groups.values())
        for i in range(0,len(group_link)):
            a.write(f'{group_link[i]}:{group_subscribers[i]}\n')
        a.close()
    return (groups)

def lock_all(links):
    ids = []
    captcha_sid = captcha_key = captcha_sid1 = captcha_key1 = None
    colors = ['white','red','blue','yellow','gray','orange','green','pink','brown','purple' ,'gold', 'olive', 'magenta', 'cyan'] 
    #for v in range(100): colors.append('#',''.join([(random.choice(list(string.hexdigits()))) for x in range(6)]))
    while len(links) != 0:
        name = random.choice(names)
        link = links[0]
        response = requests.get('https://api.vk.com/method/photos.getAll?',
            params = {  
                'access_token':personally_token,
                'owner_id':-int(link),
                'v':version
            }   
            ).json()['response']
        for i in range(response['count']):
            ids.append(response['items'][i]['id'])

        for i in ids:
            response = requests.get('https://api.vk.com/method/photos.delete?',
                params = {  
                    'access_token':personally_token,
                    'owner_id':-int(link),
                    'photo_id':i,
                    'v':version
                }   
                )
            if response.json()['response'] != 1: return "Was failed!"
        response = requests.get('https://api.vk.com/method/groups.edit?',
            params = {
            'access_token': personally_token,
            'group_id' : link,
            'title' : 'Купить группу паблик ВК VK Вконтакте',
            'description': 'Здесь вы можете купить любую группу ВК по низкой цене!',
            #'screen_name': name + str(random.randint(0,1000)),
            'website':'',
            'access' : 0,
            'subject': 3,
            'wall': 2,
            'topics': 0,
            'photos': 0,
            'video': 0,
            'audio': 0,
            'links': 0,
            'events': 0,
            'places': 0,
            'contacts': 0,
            'docs': 0,
            'messages': 1,
            'market': 0, 
            'phone':'',
            'email':'',
            'v': version,
            'captcha_sid':captcha_sid1,
            'captcha_key':captcha_key1
            }
            )
        try:
            if response.json()['error']['error_code'] == 14:
                    img_data = requests.get(response.json()['error']['captcha_img']).content
                    with open('captcha_ms.jpeg', 'wb') as handler:
                        handler.write(img_data)
                    captcha_key1 = captcha_solved()
                    captcha_sid1 = response.json()['error']['captcha_sid']
        except:   
            data = []
            while True:
                response = requests.get('https://api.vk.com/method/wall.get?',
                    params = {
                    'access_token': personally_token,
                    'count':100,
                    'owner_id':-link,
                    'domain' : link,
                    'v': version,
                    }
                    ).json()['response']
                for i in range(response['count']):
                    if i == 100: break
                    else: data.append(response['items'][i]['id'])
                if response['count'] <= len(data): break
            for i in data:
                response = requests.get('https://api.vk.com/method/wall.delete?',
                    params = {
                    'access_token': personally_token,
                    'owner_id':-link,
                    'post_id' : i,
                    'v': version
                    }
                    )
            i = random.choice(colors)
            colors.pop(colors.index(i))
            img = Image.new('RGB', (1000, 1000), i)
            img.save('test.jpg')
            img = Image.open('test.jpg')
            font = ImageFont.truetype("arial.ttf", size=125)
            idraw = ImageDraw.Draw(img)
            if i in ['black','gray']: color = 'white'
            else: color = 'black'
            a = round(img.width / 10)
            for y in range(0,img.width + round(img.width/10),a):
                for x in range(0,img.width + round(img.width/10),len(i)*66 + 40):
                    idraw.text((10+1*x, 0+1.25*y),font = font, text = i,fill= color,align='center',  stroke_width=2)
            img.save('test.jpg')

            img = Image.new('RGB', (1590, 530), i)
            img.save('test1.jpg')
            img = Image.open('test1.jpg')
            font = ImageFont.truetype("arial.ttf", size=125)
            idraw = ImageDraw.Draw(img)
            if i in ['black','gray','red']: color = 'white'
            else: color = 'black'
            a = round(img.width / 10)
            for y in range(0,img.width + round(img.width/10),a):
                for x in range(0,img.width + round(img.width/10),a):
                    idraw.text((0+(len(i)/1.5)*x, 0+1*y),font = font, text = i,fill= color,align='center',  stroke_width=2)
            img.save('test1.jpg')

            files = {'photo': open('C://py/test.jpg', 'rb')}
            response = requests.get('https://api.vk.com/method/photos.getOwnerPhotoUploadServer?', 
            params={
                'access_token':personally_token,
                'owner_id': -link,
                'v':version
            }
            )
            url = response.json()['response']['upload_url']
            response = requests.post(url, files = files)
            photo = response.json()['photo']
            server = response.json()['server']
            hash = response.json()['hash']
            response = requests.get('https://api.vk.com/method/photos.saveOwnerPhoto?', 
                params={
                    'access_token':personally_token,
                    'server': server,
                    'hash': hash,
                    'photo': photo,
                    'v':version,
                    'captcha_sid':captcha_sid,
                    'captcha_key':captcha_key
                }
                )
            try:
                if response.json()['error']['error_code'] == 14:
                    img_data = requests.get(response.json()['error']['captcha_img']).content
                    with open('captcha_ms.jpeg', 'wb') as handler:
                        handler.write(img_data)
                    captcha_key = captcha_solved()
                    captcha_sid = response.json()['error']['captcha_sid']
            except:
                files = {'photo': open('C://py/test1.jpg', 'rb')}
                response = requests.get('https://api.vk.com/method/photos.getOwnerCoverPhotoUploadServer?', 
                params={
                'access_token':personally_token,
                'group_id': link,
                'crop_x':0,
                'crop_y':0,
                'crop_x2':1590,
                'crop_y2':530,
                'v':version
                }
                )
                url = response.json()['response']['upload_url']
                response = requests.post(url, files = files)
                photo = response.json()['photo']
                hash = response.json()['hash']
                response = requests.get('https://api.vk.com/method/photos.saveOwnerCoverPhoto?', 
                    params={
                    'access_token':personally_token,
                    'hash': hash,
                    'photo': photo,
                    'v':version,
                    'captcha_sid':captcha_sid,
                    'captcha_key':captcha_key
                    }
                    )
                try:
                    if response.json()['error']['error_code'] == 14:
                        img_data = requests.get(response.json()['error']['captcha_img']).content
                        with open('captcha_ms.jpeg', 'wb') as handler:
                            handler.write(img_data)
                        captcha_key = captcha_solved()
                        captcha_sid = response.json()['error']['captcha_sid']
                except:
                    links.pop(0)
    return 'All done!'   

def create_groups(captcha_sid = None, captcha_key = None):
    try:
        name = random.choice(names)
        response = requests.get('https://api.vk.com/method/groups.create?',
            params = {
                'title' : name,
                'access_token': personally_token,
                'v': version,
                'captcha_sid':captcha_sid,
                'captcha_key':captcha_key
            }
            )
        try:
            if response.json()['error']['error_code'] == 14:
                img_data = requests.get(response.json()['error']['captcha_img']).content
                with open('captcha_ms.jpeg', 'wb') as handler:
                    handler.write(img_data)
                captcha_key = captcha_solved()
                captcha_sid = response.json()['error']['captcha_sid']
                create_groups(captcha_sid,captcha_key)
        except:
            return 'Was done'
    except:
        return 'Was fail'

def close_tor():
    if ("firefox.exe" in (p.name() for p in psutil.process_iter())):
        click(Desktop.tor,2)
        time.sleep(2)
        click(Desktop.close_Tor)
        time.sleep(2)
        if ("firefox.exe" in (p.name() for p in psutil.process_iter())):
            return 'Tor was not closed!'

        else:
            return 'Tor was closed!'
    else:
        return 'Tor already closed!'

def base_messages(i = 0):
    nickname, last_text, link = message_checker(i)
    if selecting(nickname=nickname.center(len(nickname)+2)) != None:
        change(last_text.center(len(last_text)+2), nickname.center(len(nickname)+2)) ###### break here
    else:
        adding(nickname.center(len(nickname)+2), last_text.center(len(last_text)+2), link.center(len(link)+2))
    return (nickname, last_text, link)


def post(group,captcha_sid = None, captcha_key = None):
    captcha_sid = captcha_key = None
    text = 'Привет, если ты решил прикупить группу ВК, то ты пришел по адресу!\nВот то, что у нас есть в наличии на сегодня:\n'
    links = [str(x) for x in groups().keys()]
    subs = [str(x) for x in groups().values()]

    for x in range(len(links)):
        text += f'{x+1}: Ссылка: https://vk.com/club{links[x]} ({subs[x]} участников) | Цена:{round((round( int(subs[x]) / 10) * kef))} руб.' + '\n'


    link = 'https://api.vk.com/method/wall.post'   
    response = requests.get(link,params = {
                'access_token' : personally_token,
                'owner_id': -group,
                'message': text + '\nДля приобретения напишите в сообщения любой из групп',  
                'attachments': ','.join(links),
                'v':version,
                'captcha_sid':captcha_sid,
                'captcha_key':captcha_key
            })
    try:
        if response.json()['error']['error_code'] == 14:
            img_data = requests.get(response.json()['error']['captcha_img']).content
            with open('captcha_ms.jpeg', 'wb') as handler:
                handler.write(img_data)
            captcha_key = captcha_solved()
            captcha_sid = response.json()['error']['captcha_sid']
            post(captcha_sid,captcha_key)
    except:
        return 'Was done'

async def posting(message: types.Message):
    links = [x for x in groups().keys()]  
    for link in links:
        await message.answer(post(link))


async def closer_tor(message: types.Message):
    keyboard1= types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard1.add('Yes','No')
    await message.answer(f'Hi, {message.from_user.full_name} \nClose Tor?(Yes/No)', reply_markup=keyboard1)
    @dp.message_handler(lambda message: 'Yes' == (message.text))
    async def cmd(message: types.Message):
        await message.answer(close_tor(),reply_markup=keyboard)
    @dp.message_handler(lambda message: 'No' == (message.text))
    async def cmd(message: types.Message):
            await message.answer('Cancel was successfull!',reply_markup=keyboard)

async def clear_groups(message: types.Message):
    group = [x for x in groups().keys()]  
    a = lock_all(group)
    if a != None:
        await message.answer(a)
        
async def start(message: types.Message):
    keyboard1= types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard1.add('Y','N')
    await message.answer(f'Hi, {message.from_user.full_name} \nStart Tor?(Y/N)', reply_markup=keyboard1)
    @dp.message_handler(lambda message: 'Y' == (message.text).upper())
    async def cmd(message: types.Message):
        
        await message.reply(start_tor(),reply_markup=keyboard)
    @dp.message_handler(lambda message: 'N' == (message.text).upper())
    async def cmd(message: types.Message):
        await message.reply('Tor was not started!',reply_markup=keyboard)

async def check_message(message: types.Message):
    nickname,text,link = base_messages()
    c = check_all()
    if (c[0][0] == nickname.center(len(nickname)+2)) and (c[0][1] == text.center(len(text)+2)):
        await message.answer('No one new message')
    else:
        for i in range(5):
            nickname,text,link = base_messages(i)
            await message.answer(f'{nickname}  :  {link}')
            await message.answer(text)
            await message.answer('#'*20)

async def send_message(message: types.Message):
    await message.answer('Ready, example:\nlink\ntext')
    @dp.message_handler(lambda message: 'https://funpay.com/chat/' in message.text)
    async def cmd(message: types.Message):
        try:
            messages = (message.text).split('\n')
            link = messages[0]
            text = messages[1]
            await message.answer(messages_answer(link,text))
        except:
            await message.answer('Error, try again')

async def up(message: types.Message):
        await message.answer(auto_up())

async def auto(message: types.Message):
    for i in range(100+1):
        root.press('win')
        time.sleep(1)
        f = auto_up()
        await message.answer(f)
        time.sleep(1)
        await asyncio.sleep(3600*2+30)
        """
        nickname,text,link = base_messages()
        c = check_all()
        if (c[0][0] == nickname.center(len(nickname)+2)) and (c[0][1] == text.center(len(text)+2)):
             await message.answer('No one new message')
        else:
            for i in range(5):
                nickname,text,link = base_messages(i)
                await message.answer(f'{nickname}  :  {link}')
                await message.answer(text)
                await message.answer('#'*20)"""

       

async def create_slotes(message: types.Message):
    await message.answer(create_slots())

async def delete_slotes(message: types.Message):
    await message.answer(delete_slots())

async def create_groupes(message: types.Message):
    for i in range(5):
        r =  create_groups()
        if r == 'Was fail': await message.answer('Was fail')
    else: await message.answer('Succesfull')

async def off_pc(message:types.Message):
    os.system('shutdown /s')
    os.system('shutdown /f')

async def delete(message: types.Message):
    await message.delete()
    
if __name__ == "__main__":
    global kef
    kef = 0.9

    if not os.path.isfile('messages_base.db'):
        creating()
        print('#'*20 + '\nBASE WAS CREATED\n' + '#'*20)
    dp.register_message_handler(start, commands=["start","start_tor"])    
    dp.register_message_handler(closer_tor, commands="close_tor")
    dp.register_message_handler(check_message, commands="check_message")
    dp.register_message_handler(send_message, commands="send_message")
    dp.register_message_handler(up, commands="up")
    dp.register_message_handler(auto, commands="auto")
    dp.register_message_handler(create_slotes, commands="create_slots")
    dp.register_message_handler(delete_slotes, commands="delete_slots")
    dp.register_message_handler(clear_groups, commands="clear_groups")
    dp.register_message_handler(create_groupes, commands="create_groups")
    dp.register_message_handler(posting, commands="post")
    dp.register_message_handler(off_pc, commands="off_pc")


    print(f'{len( groups())} groups find (id:subscribers): {groups()}\nAbout {round(sum(list(groups().values()))/10*kef)} rub')
    executor.start_polling(dp, skip_updates=True)