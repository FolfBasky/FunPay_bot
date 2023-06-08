import asyncio
import os
import time 
from aiogram import Bot, Dispatcher, executor, types
import logging
import sys

from sql import check_all, creating, delete_msg
from vk import *
from autogui import *
from coords import *
from data import kef


bot = Bot(token="5571779165:AAFC8iMTKtS3PHR65IxIEqaB8R7KmbdN_YE")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

async def posting(message: types.Message):
    links = [x for x in groups().keys()]  
    for link in links:
        await message.answer(post(link))

keyboard_vk = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_tor = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
yes_no = types.ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_vk.add(*["/clear_groups","/post","/create_groupes","/main","/tor"])
keyboard_tor.add(*["/start_tor","/check_message","/delete_msg","/send_message","/create_slots","/delete_slots","/up","/auto","/main","/vk"])
keyboard_main.add(*["/start","/info","/change_kef","/vk","/tor"])
yes_no.add(*["Y","N"])

def change_k(new_kef):
    with open('data.py') as a:
        data = a.read()
    with open('data.py','w') as a:
        a.write('kef = ' + str(new_kef) + '\n' + '\n'.join(data.split('\n')[1:]))

async def change_kef(message: types.Message):
    await message.answer('Enter new kef')
    @dp.message_handler()
    async def cmd(message: types.Message):
        change_k(message.text)
        global kef
        kef = float(message.text)
        await message.answer('Was done')


async def clear_groups(message: types.Message):
    group = [x for x in groups().keys()]  
    a = lock_all(group)
    if a != None:
        await message.answer(a)
        
async def start(message: types.Message):
    keyboard1= types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard1.add('Y','N')
    await message.answer(f'Hi, {message.from_user.full_name} \nStart Tor?(Y/N)', reply_markup=yes_no)
    @dp.message_handler(lambda message: 'Y' == (message.text).upper())
    async def cmd(message: types.Message):
        await message.reply(start_tor(),reply_markup=keyboard_tor)
    @dp.message_handler(lambda message: 'N' == (message.text).upper())
    async def cmd(message: types.Message):
        await message.reply('Tor was not started!',reply_markup=keyboard_tor)

async def vk_keys(message: types.Message):
    await message.answer('VK module', reply_markup=keyboard_vk)

async def tor_keys(message: types.Message):
    await message.answer('TOR module', reply_markup=keyboard_tor)

async def main_page(message: types.Message):
    await message.answer('main page', reply_markup=keyboard_main)

async def check_message(message: types.Message):
    s = check_all()
    result = []
    if s == [] or s == None: 
        for x in range(5):
            nickname, text, link = message_checker(x)
            c = 0
            if nickname == 'tps://funpay.com/chat/': 
                nickname, text, link = message_checker(x)
                c += 1
                if c >= 2: 
                    await message.answer('Failed collect messages')
                    break
            else:
                result.append([nickname,text,link])
                for par in [nickname, text, link]:
                    await message.answer(par)
                await message.answer('#'*20)
        for nickname, text, link in result[::-1]:
            adding(nickname, text, link)
        

    else:
        for x in range(5):
            nickname, text, link = message_checker(x)
            c = 0
            if nickname == 'tps://funpay.com/chat/': 
                nickname, text, link = message_checker(x)
                c += 1
                if c >= 2: 
                    await message.answer('Failed collect messages')
                    break
            s = check_all()
            if nickname in [x[1] for x in s]:
                if s[[x[1] for x in s].index(nickname)][2] == text:
                    for par in [nickname, text, link]:
                        await message.answer(par)
                    await message.answer('#'*20)
                    click(Desktop.turn_tor)
                    for *_, nickname, text, link in check_all()[-2:-5:-1]:
                        for par in [nickname, text, link]:
                            await message.answer(par)
                        await message.answer('#'*20)
                    break
                else:
                    change(text, nickname)
            else:
                adding(nickname, text, link)

            for par in [nickname, text, link]:
                    await message.answer(par)
            await message.answer('#'*20)

async def send_message(message: types.Message):
    await message.answer('Ready, example:\nlinl\ntext')
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
    for _ in range(100+1):
        root.press('win')
        time.sleep(1)
        f = auto_up()
        await message.answer(f)

        for _ in range(8):
            s = check_all()
            result = []
            if s == [] or s == None: 
                for x in range(5):
                    nickname, text, link = message_checker(x)
                    c = 0
                    if nickname == 'tps://funpay.com/chat/': 
                        nickname, text, link = message_checker(x)
                        c += 1
                        if c >= 2: 
                            await message.answer('Failed collect messages')
                            
                            break
                    else:
                        result.append([nickname,text,link])
                for nickname, text, link in result[::-1]:
                    adding(nickname, text, link)

            else:
                for x in range(5):
                    nickname, text, link = message_checker(x)
                    c = 0
                    if nickname == 'tps://funpay.com/chat/': 
                        nickname, text, link = message_checker(x)
                        c += 1
                        if c >= 2: 
                            await message.answer('Failed collect messages')
                            break
                    s = check_all()
                    if nickname in [x[1] for x in s]:
                        if s[[x[1] for x in s].index(nickname)][2] == text:
                            click(Desktop.turn_tor)
                            break
                        else:
                            change(text, nickname)
                            await message.answer('New message from old user')
                    else:
                        adding(nickname, text, link)
                        await message.answer('New message from new user')
            await asyncio.sleep(14*60)

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
    await message.delete()
    os.system('shutdown /s')
    os.system('shutdown /f')

async def info(message:types.Message):
    await message.answer(f'{len( groups())} groups find (id:subscribers): {groups()}\nAbout {round(sum(list(groups().values()))/10*kef)} rub')

async def delete_last(message: types.Message):
    delete_msg()
    await message.answer('Last 5 rows was deleted!')

if not os.path.isfile('messages_base.db'):
    creating()
    print('#'*20 + '\nBASE WAS CREATED\n' + '#'*20)

dp.register_message_handler(start, commands=["start","start_tor"])    
dp.register_message_handler(check_message, commands="check_message")
dp.register_message_handler(delete_last, commands="delete_msg")
dp.register_message_handler(send_message, commands="send_message")
dp.register_message_handler(up, commands="up")
dp.register_message_handler(auto, commands="auto")
dp.register_message_handler(create_slotes, commands="create_slots")
dp.register_message_handler(delete_slotes, commands="delete_slots")
dp.register_message_handler(clear_groups, commands="clear_groups")
dp.register_message_handler(create_groupes, commands="create_groups")
dp.register_message_handler(posting, commands="post")
dp.register_message_handler(off_pc, commands="off_pc")
dp.register_message_handler(info, commands="info")
dp.register_message_handler(vk_keys, commands="vk")
dp.register_message_handler(tor_keys, commands="tor")
dp.register_message_handler(main_page, commands="main")
dp.register_message_handler(change_kef, commands="change_kef")

print(f'{len( groups())} groups find (id:subscribers): {groups()}\nAbout {round(sum(list(groups().values()))/10*kef)} rub')
executor.start_polling(dp, skip_updates=True)