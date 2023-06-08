import pyautogui as root
import time 
import pyperclip 
import requests
import psutil 
import keyboard as keyboard_button

from coords import *
from data import *
from vk import *
from sql import *


def click(s,k=1): # s = x,y , k = amount of clicks
    x,y = s
    root.click(x,y,clicks = k)

def paste(s,text,enter = True): # s = x,y , text = your text
    x,y = s
    pyperclip.copy(text)
    root.click(x,y,3)
    time.sleep(0.5)
    keyboard_button.press_and_release('ctrl+v')
    if enter == True: keyboard_button.press_and_release('enter')

def start_tor():
    click(Desktop.tor,2)
    time.sleep(3)
    click(Tor.new_persona)
    time.sleep(20)
    paste(Tor.link_coordinates,Tor.funpay)
    time.sleep(5)
    click(Tor.link_coordinates)
    root.press('enter')
    time.sleep(7)
    click(Tor.enter)
    time.sleep(12)
    paste(Tor.login_coordinates,login,False)
    time.sleep(0.15)
    click(Tor.login_coordinates)
    time.sleep(0.5)
    paste(Tor.password_coordinates,password, False)
    time.sleep(100) # Captcha 
    paste(Tor.number_coordinates,number)
    time.sleep(7)

    click(Tor.link_coordinates, 1)
    time.sleep(0.5)
    root.hotkey('ctrl','c')
    link = pyperclip.paste()

    click(Desktop.turn_tor)
    return 'Enter was done' if 'https://funpay.com/' == link else 'Fail' 

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
    if scroll == 0:
        click(Desktop.tor,2)
        time.sleep(1)
        paste(Tor.link_coordinates,Tor.chat_link)
    
    time.sleep(7)
    root.moveTo(Tor.chat_new)
    
    if scroll != 0 : time.sleep(1)
    root.move(0,63*scroll)
    if scroll != 0 : time.sleep(1)
    root.click()
    time.sleep(7)
    
    root.moveTo(Tor.nick_start)
    root.dragTo(Tor.nick_end, duration=0.5, button='left')
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

    
    if scroll == 4: click(Desktop.turn_tor)
    """
    text = text.replace('\r\n',' ')
    
    for months in range(1,13):
        for days in range(1,32):
            times = (f'{str(days).rjust(2,"0")}.{str(months).rjust(2,"0")}.{str(round(time.time() / 31536000) + 1969)[-1:-2]}')
            text = text.replace(times,'')

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
        elif f'{login} оплатил заказ ' in funpay_order_text:
            funpay_order = [text.find('FunPay оповещение')-1,text.find("».",text.find('FunPay оповещение'))+2]
            funpay_order_text = text[funpay_order[0] + funpay_order[1]]
        text = text[:funpay_order[0]] + ' *операции на сайте* ' + text[funpay_order[1]:]
        
        time.sleep(0.05)"""
    return (nick[2:],text,link)

def messages_answer(link,text1): #text = text that bot send user
    time.sleep(2)
    click(Desktop.tor,2)
    time.sleep(1)
    paste(Tor.link_coordinates,link)
    time.sleep(5)
    if link == Tor.chat_link:
        click(Tor.chat_new)
        time.sleep(5)
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

    for k,i in enumerate(groups_data):

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
    time.sleep(7)

    for _ in groups_data:
        click(Tor.slots.slot)
        time.sleep(5)
        root.scroll(-10000)
        time.sleep(0.3)
        click(Tor.slots.delete)
        time.sleep(0.5)
        click(Tor.slots.confirm_delete)
        time.sleep(3)
    else:
        click(Desktop.turn_tor)
    return 'All slots was deleted!'

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