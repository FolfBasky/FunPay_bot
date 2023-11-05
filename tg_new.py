import asyncio
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from sql import *
from vk import *
from funpay import *
from data import kef

bot = Bot(token="5571779165:AAFC8iMTKtS3PHR65IxIEqaB8R7KmbdN_YE")
admin_chat_id = -778858479
dp = Dispatcher(bot, storage=MemoryStorage())
admin_id = 879165748

async def posting(message: types.Message):
    links = [x for x in groups().keys()]  
    for link in links:
        post(link)
        await message.answer(f'In {link} was succesfully post created')

keyboard_vk = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_tor = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
yes_no = types.ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_vk.add(*["/info","/get_vk_profiles","/add_account_vk","/delete_vk_profile","/set_vk_profile","/clear_groups","/post","/create_groupes", "/kill_admins_vk","/main","/tor"])
keyboard_tor.add(*["/start_bot","/check_message","/check_sales", "/refund_orders","/check_orders", "/complete_orders","/send_message","/create_slots","/delete_slots","/edit_lot","/check_lots","/get_balance","/check_balance_operations","/withdrow_balance", "/cancel_operations_balances","/up","/auto","/check_ip","/check_feedbacks","/logout","/register_account","/main","/vk"])
keyboard_main.add(*["/start_bot","/change_kef","/get_account", "/add_account","/edit_account","/delete_account","/vk","/tor"])
yes_no.add(*["Y","N"])

@dp.message_handler(commands='cancel',state='*')
async def register_account_(message: types.Message, state: FSMContext):
    await message.answer('Canceled!')
    await state.finish()

def change_k(new_kef):
    with open('data.py') as a:
        data = a.read()
    with open('data.py','w') as a:
        a.write('kef = ' + str(new_kef) + '\n' + '\n'.join(data.split('\n')[1:]))

class Kef_states(StatesGroup):
    enter_kef = State()

async def change_kef(message: types.Message):
    await message.answer('Enter new kef')
    await Kef_states.enter_kef.set()

@dp.message_handler(lambda message: message.text.replace('.','').isdigit(), state=Kef_states.enter_kef) 
async def cmd(message: types.Message, state: FSMContext):
    change_k(message.text)
    global kef
    kef = float(message.text)
    await message.answer('Was done')
    await state.finish()

@dp.message_handler(state = Kef_states.enter_kef)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Not correct answer!')
    await state.finish()

async def clear_groups(message: types.Message):
    group = [x for x in groups().keys()]  
    a = lock_all(group)
    if a != None:
        await message.answer(a)

class Start_states(StatesGroup):
    choice = State()

async def start(message: types.Message):
    if message.from_user.id == admin_id:
        keyboard1= types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard1.add('Y','N')
        await message.answer(f'Hi, {message.from_user.full_name}! \nStart Bot?(Y/N)', reply_markup=yes_no)
        await Start_states.choice.set()

@dp.message_handler(lambda message: 'Y' == (message.text).upper(), state = Start_states.choice)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Conecting...')
    global session_status
    #try:
    ''' if session_status: 
            await message.answer('Session is alredy active!')
        else:'''
    res = logging_()
    if res == None:
        await message.reply('Session is active',reply_markup=keyboard_tor)
        session_status = True
    else:
        await message.reply(res, reply_markup=keyboard_main)
        session_status = False
    ''' except:
        session_status = False
    finally:'''
    await state.finish()

@dp.message_handler(lambda message: 'N' == (message.text).upper(), state = Start_states.choice)
async def cmd(message: types.Message, state: FSMContext):
    await message.reply('Session was not started!',reply_markup=keyboard_tor)
    await state.finish()

@dp.message_handler(state = Start_states.choice)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Not correct answer!', reply_markup=keyboard_tor)
    await state.finish()

@dp.message_handler(commands='logout')
async def logouting(message: types.Message):
    global auto_while, session_status
    auto_while = False
    try:
        res = logout()
        if res[0] and session_status:
            await message.answer('Succesfull')
            session_status = False
        else: await message.answer('Failed!\n{}'.format(res[1]))
    except Exception as e:
        await message.answer(e)

class RegisterAccountStates(StatesGroup):
    nickname = State()
    email = State()
    phone = State()
    link = State()
    code = State()

@dp.message_handler(commands='register_account', state='*')
async def register_account_(message: types.Message):
    await message.answer('Enter nickname:')
    await RegisterAccountStates.nickname.set()

@dp.message_handler(lambda message: len(message.text) >= 3 and len(message.text) <= 20, state=RegisterAccountStates.nickname)
async def register_account_(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text
    await message.answer('Enter email:')
    await RegisterAccountStates.email.set()

@dp.message_handler(state=RegisterAccountStates.nickname)
async def register_account_(message: types.Message):
    await message.answer('Invalid data! Nickname should be 3-20 charackters')

@dp.message_handler(lambda message: '@' in message.text , state=RegisterAccountStates.email)
async def register_account_(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer('Enter phone number:')
    await RegisterAccountStates.phone.set()

@dp.message_handler(state=RegisterAccountStates.email)
async def register_account_(message: types.Message):
    await message.answer('Invalid data! "@" should be in email!')

@dp.message_handler(lambda message: re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', message.text), state=RegisterAccountStates.phone)
async def register_account_(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            email = data['email']
            password = generate_random_string(4)
            nickname = data['nickname']
            await message.answer('Creating account! Wait...')
            if not register_account(nickname, email, password): raise Exception
            else: await message.answer('Account was succesfully created!')
        
        
            data['phone'] = message.text
            if not add_user_profile(1,email, password, data['phone']): raise Exception

        await message.answer('Data was succesfully writed! Enter link from email:')

        

    except Exception as e:
        await message.answer(e)
        await state.finish()

    await RegisterAccountStates.link.set()

@dp.message_handler(state=RegisterAccountStates.phone)
async def register_account_(message: types.Message):
    await message.answer('Invalid data! Example: "89000000000"')

@dp.message_handler(lambda message: 'https://funpay.com' in message.text, state=RegisterAccountStates.link)
async def register_account_(message: types.Message, state: FSMContext):
    activate_account(message.text)
    await message.answer('Account was succesfully activated!')
    await message.answer('Last step! Wait while bot solved the test...')
    async with state.proxy() as data:
        phone = data['phone']
        set_active_status_accounts()
        set_account_active(login=data['email'], active=1)
    try:
        if not pass_the_test(phone): 
            await message.answer('Enter code, that was sended on you number:')
            await RegisterAccountStates.code.set()
        else: 
            await message.answer('Something was wrong!')
    except Exception as e:
        await message.answer(e)

@dp.message_handler(state=RegisterAccountStates.link)
async def register_account_(message: types.Message):
    await message.answer('Invalid data! Enter correct link')

@dp.message_handler(lambda message: message.text.isdigit(),state=RegisterAccountStates.code)
async def register_account_(message: types.Message, state: FSMContext):
    if not pass_the_test_code(message.text): await message.answer('Phone was succesfully confirmed!')
    else: await message.answer('Something was wrong!')
    await state.finish()

@dp.message_handler(state=RegisterAccountStates.code)
async def register_account_(message: types.Message):
    await message.answer('Invalid data! Enter correct code!')


async def vk_keys(message: types.Message):
    await message.answer('VK module', reply_markup=keyboard_vk)
    #await message.answer(message.chat.id)

async def tor_keys(message: types.Message):
    await message.answer('TOR module', reply_markup=keyboard_tor)

async def main_page(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer('main page', reply_markup=keyboard_main)

async def check_message(message: types.Message):
    try:
        result = collect_chats()
        for x in result:
            msg = check_messages(x[2])
            if len(msg) >= 1000: msg = msg[-1000:]
            await message.answer('\n'.join(msg))
            await message.answer(x[2])
            await message.answer('#'*20)
            await asyncio.sleep(1) 
    except Exception as e:
        await message.answer(e)

class Msg_states(StatesGroup):
    link = State()
    text = State()

async def send_message(message: types.Message, state: FSMContext):
    await message.answer('Enter link')
    await Msg_states.link.set()

@dp.message_handler(lambda message: 'https://funpay.com/chat/' in message.text, state=Msg_states.link)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
    await message.answer('Enter text')
    await Msg_states.text.set()

@dp.message_handler(lambda message: 'https://funpay.com/chat/' not in message.text, state=Msg_states.link)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Not correct link!', reply_markup=keyboard_tor)
    await state.finish()

@dp.message_handler(lambda message: 'cancel' not in message.text.lower() and '/send_message' not in message.text.lower(), state=Msg_states.text)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        link = data['link']
        text = message.text
    try:
        res = message_answer_r(link,text)
        await message.answer(res)
    except Exception as res:
        await message.answer(res)
    await state.finish()

@dp.message_handler(lambda message: '/cancel' in message.text or '/send_message' in message.text.lower(), state=Msg_states.text)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!', reply_markup=keyboard_tor)
    await state.finish()

async def up(message: types.Message):
    await message.answer(up_lots())

async def auto(message: types.Message):
    global auto_message
    try:
        if auto_message:
            await message.answer('Bot have restart succesfully!')
        else:
            await message.answer('Bot havent restart!')
    except:
        pass 
    finally:
        auto_message = False
    storage_last_message = []
    global auto_while
    auto_while = True
    while auto_while:
        try:
            lst = up_lots()
        except requests.ConnectionError:
            await message.answer('Bad internet, bot will restart after 10 minutes!')
            await asyncio.sleep(60*10)
            auto_message = True
            await auto()
        if 'Slot' in lst: await message.answer(lst)
        elif 'Fail' == lst:
            await message.answer('Session was down\nWaiting...')
            if not (result := logging_()): 
                await message.answer('Session is working')
            else:
                await message.answer(result)
                await asyncio.sleep(5*60)
                await auto(message)
        last_msgs = collect_chats()[:5]
        for x in last_msgs:
            if x[1] in storage_last_message:
                break
            else:
                storage_last_message.append(x[1])
                await message.answer(f'{x[2]} : {x[0]}')
                await message.answer(x[1])
                await message.answer('#'*20)
        await asyncio.sleep(20)

async def create_slotes(message: types.Message):
    await message.answer(create_lot())

async def delete_slotes(message: types.Message):
    await message.answer(delete_slots())

async def create_groupes(message: types.Message):
    for _ in range(5):
        r =  create_groups()
        if r == 'Was fail': await message.answer('Was fail')
    else: await message.answer('Succesfull')

async def off_pc(message:types.Message):
    await message.delete()
    os.system('shutdown /s')
    os.system('shutdown /f')

async def info(message:types.Message):
    try:
        accs = select_all_vk_profiles()
        all_suma = 0
        for acc in accs:
            login = ('#'*5) + acc['login'] + ('#'*5)
            set_active_status_vk_accounts()
            choice_active_status_vk_account(login)
            data = groups()
            summa = round(sum(list(data.values()))/10*kef)
            await message.answer(f'{login}\n{len(data)} groups find (id:subscribers): {data}\nAbout {summa} rub')
            all_suma += summa
        await message.answer(f'All is {all_suma} rub') 
    except Exception as e:
        await message.answer(e)



async def check_sales(message: types.Message):
    for x in check_orders_or_sales(sales=True):
        await message.answer(f'{x[0]} - {x[1]}\n{x[2]}\n{x[3]}\n{x[4]}\n{x[5]}')

async def check_orders(message: types.Message):
    for x in check_orders_or_sales(sales=False):
        await message.answer(f'{x[0]} - {x[1]}\n{x[2]}\n{x[3]}\n{x[4]}\n{x[5]}')

async def check_lots(message: types.Message):
    d = check_lots_r()
    for x in d.keys():
        await message.answer(f'{d[x]}\n{x}')
        await asyncio.sleep(0.5)

class Edit_lot_states(StatesGroup):
    lot_id = State()
    deleted = State()
    followers = State()
    summary = State()
    desc = State()
    price = State()

async def edit_lot(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*[x for x in check_lots_r().keys()], '/cancel')
    await message.answer('Enter lot id', reply_markup=markup)
    await Edit_lot_states.lot_id.set()

@dp.message_handler(lambda message: message.text != '/cancel', state=Edit_lot_states.lot_id)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['offer_id'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*['0','1'], '/cancel')
    await message.answer('Enter deleted status', reply_markup=markup)
    await Edit_lot_states.deleted.set()

@dp.message_handler(lambda message: message.text != '/cancel', state=Edit_lot_states.deleted)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['deleted'] = message.text
        if data['deleted'] == '1':
            await message.answer(edit_lot_r(data['offer_id'], data['deleted']), reply_markup=keyboard_tor)
            await state.finish()
        else:
            await message.answer('Enter count followers')
            await Edit_lot_states.followers.set()

@dp.message_handler(lambda message: message.text != '/cancel', state=Edit_lot_states.followers)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['followers'] = message.text
    await message.answer('Enter summary')
    await Edit_lot_states.summary.set()

@dp.message_handler(lambda message: message.text != '/cancel', state=Edit_lot_states.summary)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['summary'] = message.text
    await message.answer('Enter desc')
    await Edit_lot_states.desc.set()

@dp.message_handler(lambda message: message.text != '/cancel', state=Edit_lot_states.desc)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Enter price')
    await Edit_lot_states.price.set()

@dp.message_handler(lambda message: message.text != '/cancel', state=Edit_lot_states.price)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
        await message.answer(edit_lot_r(**data._data), reply_markup=keyboard_tor)
    await state.finish()

@dp.message_handler(commands='cancel', state='*')
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!', reply_markup=keyboard_tor)
    await state.finish()

async def check_ip_r(message:types.Message):
    try:
        ip = session.get("http://httpbin.org/ip", timeout=15).text
        await message.answer('IP:' + re.search(r'\d{2,}.\d{2,}.\d{2,}.\d{2,}', ip)[0] )
    except:
        await message.answer('Bad internet connection!')    

async def get_balance(message:types.Message):
    await message.answer(get_balance_r())

class Withdrowing_states(StatesGroup):
    enter_wall = State()

async def withdrow_balance(message:types.Message, state: FSMContext):
    await message.answer('Enter wallet')
    await Withdrowing_states.enter_wall.set()

@dp.message_handler( state = Withdrowing_states.enter_wall)
async def cmd(message: types.Message, state: FSMContext):
    res = withdrow_money(message.text)
    await message.answer(res)
    if res == 'Money was sended!':
        if not get_first_active_account_info()['card_number']:
            card = message.text
            if len(card) == 16 and card.isdigit():
                add_card_number(get_first_active_account_info()['login'], card)
    await state.finish()

@dp.message_handler(commands='cancel', state = Withdrowing_states.enter_wall)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!', reply_markup=keyboard_tor)
    await state.finish()

async def check_balance_operations(message:types.Message):
    for x in check_balance_operation():
        await message.answer(x)

class Cancel_balance_operation_states(StatesGroup):
    oper_id = State()

async def cancel_operations_balances(message:types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*[x.split('\n')[-1] for x in check_balance_operation()], '/cancel')
    await message.answer('Enter operation id', reply_markup=markup)
    await Cancel_balance_operation_states.oper_id.set()

@dp.message_handler( state = Cancel_balance_operation_states.oper_id)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer(cancel_balance_operation(message.text), reply_markup=keyboard_tor)
    await state.finish()

@dp.message_handler(commands='cancel', state = Cancel_balance_operation_states.oper_id)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!', reply_markup=keyboard_tor)
    await state.finish()

class Complete_order_states(StatesGroup):
    oper_id = State()

async def complete_orders(message: types.Message):
    await message.answer('Enter oper id')
    await Complete_order_states.oper_id.set()

@dp.message_handler( state = Complete_order_states.oper_id)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer(complete_order(message.text), reply_markup=keyboard_tor)
    await state.finish()

@dp.message_handler(commands='cancel', state = Complete_order_states.oper_id)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!', reply_markup=keyboard_tor)
    await state.finish()

class Refund_orders_states(StatesGroup):
    oper_id = State()

async def refund_orders(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/cancel')
    await message.answer('Enter operation hashtag: ')
    await Refund_orders_states.oper_id.set()

@dp.message_handler( state=Refund_orders_states.oper_id)
async def cmd(message: types.Message, state: FSMContext):
    try:
        await message.answer(refund_order(message.text), reply_markup=keyboard_tor)
    except Exception as e:
        await message.answer(e, reply_markup=keyboard_tor)
    await state.finish()

@dp.message_handler(commands='cancel', state=Refund_orders_states.oper_id)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!', reply_markup=keyboard_tor)
    await state.finish()

async def check_feedbacks(message: types.Message):
    for feedback in check_feedback():
        await message.answer('\n'.join(feedback))
        await message.answer('#'*20)

class Funpay_Account_states(StatesGroup):
    login = State()
    password = State()
    number = State()
    card = State()

async def funpay_account(message: types.Message):
    await message.answer('Enter login')
    await Funpay_Account_states.login.set()

@dp.message_handler(state=Funpay_Account_states.login)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    await message.answer('Enter password')
    await Funpay_Account_states.next()

@dp.message_handler(commands='cancel', state=Funpay_Account_states.login)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!')
    await state.finish()

@dp.message_handler( state=Funpay_Account_states.password)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await message.answer('Enter numbers of the phone')
    await Funpay_Account_states.next()

@dp.message_handler(commands='cancel', state=Funpay_Account_states.password)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!')
    await state.finish()

@dp.message_handler( state=Funpay_Account_states.number)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    await message.answer('Enter numbers of the card or /skip')
    await Funpay_Account_states.next()

@dp.message_handler(commands='cancel', state=Funpay_Account_states.number)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!')
    await state.finish()

@dp.message_handler(lambda message: 'cancel' not in message.text.lower() and '/' not in message.text.lower(), state=Funpay_Account_states.card)
async def cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['card'] = message.text
        if add_user_profile(1, data['login'], data['password'], data['number'], data['card']):
            await message.answer('Data was succesfully writed!')
        else:
            await message.answer('Something were wrong!')
    await state.finish()

@dp.message_handler(commands='cancel', state=Funpay_Account_states.card)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Canceled!')
    await state.finish()

@dp.message_handler(commands='skip', state=Funpay_Account_states.card)
async def cmd(message: types.Message, state: FSMContext):
    await message.answer('Card was skipped!')
    async with state.proxy() as data:
        if add_user_profile(1, data['login'], data['password'], data['number']):
            await message.answer('Data was succesfully writed!')
        else:
            await message.answer('Something were wrong!')
    await state.finish()

async def get_account(message: types.Message):
    for account in get_all_profiles()[::-1]:
        await message.answer(f'active: {bool(account["active"])}\nlogin: {account["login"]}\npassword: {account["password"]}\nphone: {account["phone_number"]}\ncard: {account["card_number"]}')
        await message.answer('#'*20)

class Funpay_Account():
    active = str()
    login = str()

async def edit_account(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(*[types.InlineKeyboardButton(text=x['login'], callback_data=x['login']+'_edit') for x in get_all_profiles()])
    await message.answer('Choice account', reply_markup=markup)
    global funpay_acc
    funpay_acc = Funpay_Account()

@dp.callback_query_handler(text=[x['login']+'_edit' for x in get_all_profiles()])
async def send_random_value(call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='0',callback_data='0'+'_edit'),types.InlineKeyboardButton(text='1',callback_data='1'+'_edit'))
    global funpay_acc
    funpay_acc.login = call.data[:-5]
    await call.message.answer('Enter active status', reply_markup=markup)

@dp.callback_query_handler(text=['0'+'_edit','1'+'_edit'])
async def send_random_value(call: types.CallbackQuery):
    global funpay_acc
    funpay_acc.active = call.data[:-5]
    set_active_status_accounts()
    set_account_active(login = funpay_acc.login, active = funpay_acc.active)
    await call.message.answer('Succesfull!')

async def delete_account(message:types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(*[types.InlineKeyboardButton(text=x['login'], callback_data=x['login']+'_delete') for x in get_all_profiles()])
    await message.answer('Choice account', reply_markup=markup)

@dp.callback_query_handler(text=[x['login']+'_delete' for x in get_all_profiles()])
async def send_random_value(call: types.CallbackQuery):
    if delete_user(call.data[:-7]):
        await call.message.answer('Succesfull!')
    else:
        await call.message.answer('Failed!')

class VK_Account(StatesGroup):
    login = State()
    access_token = State()
    user_id = State()

async def start_adding_vk_account(message: types.Message):
    """
    Sends an introduction message to the user and prompts them to enter their VK account login
    """
    await message.answer('Hey! I need to gather some information in order to add a new VK account.\nPlease enter your VK login:')
    await VK_Account.login.set()

@dp.message_handler(state=VK_Account.login)
async def receive_access_token(message: types.Message, state:FSMContext):
    """
    Stores the user's VK login as state and prompts them to enter their VK account access token
    """
    async with state.proxy() as data:
        data['login'] = message.text
    await message.answer('Great! Now enter your VK access token:')
    await VK_Account.access_token.set()

@dp.message_handler(state=VK_Account.access_token)
async def receive_user_id(message: types.Message, state:FSMContext):
    """
    Stores the user's VK access token as state and prompts them to enter their VK user ID
    """
    async with state.proxy() as data:
        data['access_token'] = message.text
    await message.answer('Almost done! Enter your VK user ID:')
    await VK_Account.user_id.set()

@dp.message_handler(state=VK_Account.user_id)
async def add_vk_accounts(message: types.Message, state:FSMContext):
    """
    Stores the user's VK user ID as state and passes all gathered data to add_account_vk() before finishing the conversation
    """
    async with state.proxy() as data:
        data['user_id'] = message.text
        add_vk_account(login=data['login'], access_token=data['access_token'], user_id=int(data['user_id']))
    await message.answer('Success! Your VK account has been added.')
    await state.finish()

@dp.message_handler(commands='cancel', state='*')
async def cancel_adding_vk_account(message: types.Message, state: FSMContext):
    """
    Ends the conversation and cancels the addition of a new VK account
    """
    await message.answer('Adding a new VK account has been canceled.')
    await state.finish()

async def delete_vk_profile(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(*[types.InlineKeyboardButton(text=x['login'], callback_data=x['login']+'_delete_vk_acc') for x in select_all_vk_profiles()])
    await message.answer('Select account to deleting...', reply_markup=markup)

@dp.callback_query_handler(text=[x['login']+'_delete_vk_acc' for x in select_all_vk_profiles()])
async def calc(call: types.CallbackQuery):
    delete_vk_account(login=call.data.split("_")[0])
    await call.message.answer(f'Account {call.data.split("_")[0]} was deleted!')


vk_account_data = [x['login']+'_seting_vk_acc' for x in select_all_vk_profiles()]

async def set_vk_profile(message:types.Message):
    global vk_account_data
    vk_account_data = [x['login']+'_seting_vk_acc' for x in select_all_vk_profiles()]
    markup = types.InlineKeyboardMarkup()
    markup.add(*[types.InlineKeyboardButton(text=x['login'], callback_data=x['login']+'_seting_vk_acc') for x in select_all_vk_profiles()])
    await message.answer('Select account...', reply_markup=markup)

@dp.callback_query_handler(text=vk_account_data)
async def calc(call: types.CallbackQuery):
    set_active_status_vk_accounts()
    choice_active_status_vk_account(login=call.data.split("_")[0])
    await call.message.answer(f'Account {call.data.split("_")[0]} was choiced!')

async def get_vk_profiles(message:types.Message):
    data = select_all_vk_profiles()
    for result in data:
        text = f'active: {bool(result["active"])}\nlogin: {result["login"]}\naccess token: {result["access_token"]}\nuser id: {result["user_id"]}'
        await message.answer(text)
        await message.answer('#'*20)

async def kill_admins_vk(message:types.Message):
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Accept', callback_data='accept_kill_admin'))
    await message.answer('Kill admins? Press the button to continue...', reply_markup=markup)

@dp.callback_query_handler(text='accept_kill_admin')
async def cmd(call: types.CallbackQuery):
    await call.message.answer('Start clearing groups on the account: "{}"'.format(get_first_active_account_vk_info()["login"]))
    main_admins()
    await call.message.answer('Done!')

async def on_startup(dp):
    await bot.send_message(admin_chat_id, "Bot's working!")


def message_handelers_registers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start","start_bot"])
    dp.register_message_handler(create_groupes, commands="create_groupes")
    dp.register_message_handler(check_message, commands="check_message")
    dp.register_message_handler(create_slotes, commands="create_slots")
    dp.register_message_handler(delete_slotes, commands="delete_slots")
    dp.register_message_handler(clear_groups, commands="clear_groups")
    dp.register_message_handler(check_orders, commands="check_orders")
    dp.register_message_handler(send_message, commands="send_message")
    dp.register_message_handler(check_sales, commands="check_sales")
    dp.register_message_handler(change_kef, commands="change_kef")
    dp.register_message_handler(check_ip_r, commands="check_ip")
    dp.register_message_handler(main_page, commands="main")
    dp.register_message_handler(off_pc, commands="off_pc")
    dp.register_message_handler(posting, commands="post")
    dp.register_message_handler(tor_keys, commands="tor")
    dp.register_message_handler(vk_keys, commands="vk")
    dp.register_message_handler(info, commands="info")
    dp.register_message_handler(auto, commands="auto")
    dp.register_message_handler(up, commands="up")
    dp.register_message_handler(check_lots, commands="check_lots")
    dp.register_message_handler(edit_lot, commands="edit_lot")
    dp.register_message_handler(get_balance, commands="get_balance")
    dp.register_message_handler(withdrow_balance, commands="withdrow_balance")
    dp.register_message_handler(check_balance_operations, commands="check_balance_operations")
    dp.register_message_handler(complete_orders, commands="complete_orders")
    dp.register_message_handler(refund_orders, commands="refund_orders")
    dp.register_message_handler(cancel_operations_balances, commands="cancel_operations_balances")
    dp.register_message_handler(check_feedbacks, commands="check_feedbacks")
    dp.register_message_handler(funpay_account, commands="add_account")
    dp.register_message_handler(get_account, commands="get_account")
    dp.register_message_handler(edit_account, commands="edit_account")
    dp.register_message_handler(delete_account, commands="delete_account")
    dp.register_message_handler(start_adding_vk_account, commands="add_account_vk")
    dp.register_message_handler(get_vk_profiles, commands="get_vk_profiles")
    dp.register_message_handler(delete_vk_profile, commands="delete_vk_profile")
    dp.register_message_handler(set_vk_profile, commands="set_vk_profile")
    dp.register_message_handler(kill_admins_vk, commands="kill_admins_vk")

if __name__ == '__main__':
    message_handelers_registers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, allowed_updates=True)