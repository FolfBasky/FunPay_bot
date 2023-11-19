import requests
import random
import string
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
from PIL import Image, ImageDraw, ImageFont
from data import kef
from sql import get_first_active_account_vk_info, set_active_status_vk_accounts, choice_active_status_vk_account
from tqdm import tqdm
import time
from bs4 import BeautifulSoup

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def get_data():
    #set_active_status_vk_accounts()
    #choice_active_status_vk_account('john')
    data = get_first_active_account_vk_info()
    access_token = data['access_token']
    user_id = data['user_id']
    return access_token, user_id

version = '5.131'

def captcha_solved():
    api_key = '9202b639f977797ed5b756b0c3af9327'
    captcha_fp = open('captcha_ms.jpeg', 'rb')
    client = AnticaptchaClient(api_key)
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task)
    job.join()
    print('Captcha key = ',job.get_captcha_text())
    return (job.get_captcha_text())

def generate_random_string(lenght):
    vowels = [x for x in list(string.ascii_lowercase) if x in 'aeiouy']
    consonants = [x for x in list(string.ascii_lowercase) if x not in 'aeiouy']

    result = ''
    for _ in range(lenght):
        result += random.choice(consonants)
        result += random.choice(vowels)
    else:
        for _ in range(lenght-1): result += random.choice(list(string.digits))

    return result.capitalize()
names = []
for i in range(200):
    names.append(generate_random_string(3))

def get_admins_groups():
    personally_token, user_id = get_data()
    response = requests.get('https://api.vk.com/method/groups.get?',
        params = {
        'user_id' : user_id,
        'extended' : 0,
        'filter' : 'admin',
        'access_token': personally_token,
        'v': version
        }
        )
    result = response.json()['response']['items']
    try:
        #result = 
        #for x in [174746452,215991768,218599370, 218819870, 218819887]:
        #    result.remove(x)
        #result = 
        #result.remove(174746452)
        ...
    except:
        pass
    return result

def count_subscribers(link):
    personally_token, user_id = get_data()
    response = requests.get('https://api.vk.com/method/groups.getMembers?',
        params = {
        'group_id' : link,
        'access_token': personally_token,
        'v': version
        })
    try:
        count_sub = (response.json()['response']['count'])
        if count_sub > 500 and count_sub < 100000: return(count_sub)
    except:
        pass

def groups() -> dict:
    '{id:subs}'
    admins_groups = get_admins_groups()
    grops_count_subscribers = []
    for id in admins_groups:
        grops_count_subscribers.append(count_subscribers(id))
    groups = dict(zip(admins_groups,grops_count_subscribers))
    groups = {i: j for i, j in groups.items() if j!=None }
    return groups

def create_photos():
    variant = 1 # 0 - colourfull, 1 - black
    if variant == 0:
        colors = ['white','red','blue','yellow','gray','orange','green','pink','brown','purple' ,'gold', 'olive', 'magenta', 'cyan'] 
        i = random.choice(colors)
        colors.pop(colors.index(i))
    elif variant == 1: 
        colors = ['black']
        i = colors[0]
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

def main_photo(personally_token, link, captcha_key='',captcha_sid=''):
    files = {'photo': open('photos/image_avatar.jpg', 'rb')}
    response = requests.get('https://api.vk.com/method/photos.getOwnerPhotoUploadServer?', 
    params={
        'access_token':personally_token,
        'owner_id': -link,
        'v':version,
        'captcha_sid':captcha_sid,
        'captcha_key':captcha_key
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
            return main_photo(personally_token, link, captcha_key=captcha_key,captcha_sid=captcha_sid)
    except:
        return True

def edit_group_info(personally_token, link, captcha_key='',captcha_sid=''):
    response = requests.get('https://api.vk.com/method/groups.edit?',
        params = {
        'access_token': personally_token,
        'group_id' : link,
        'title' : ex.word,
        'description': '',
        #'screen_name': name + str(random.randint(0,1000)),
        'website':'',
        'access' : 2,
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
            edit_group_info(personally_token, link, captcha_key=captcha_key, captcha_sid=captcha_sid)
    except:   
        return True

def back_photo(personally_token,link, captcha_key='',captcha_sid=''):
    files = {'photo': open('photos/image_poster.jpg', 'rb')}
    response = requests.get('https://api.vk.com/method/photos.getOwnerCoverPhotoUploadServer?', 
    params={
    'access_token':personally_token,
    'group_id': link,
    'crop_x':0,
    'crop_y':0,
    'crop_x2':1590,
    'crop_y2':530,
    'v':version,
    'captcha_sid':captcha_sid,
    'captcha_key':captcha_key
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
            return back_photo(personally_token, link, captcha_key=captcha_key,captcha_sid=captcha_sid)   
    except:
        return True

def delete_photos_from_group(personally_token, link):
    ids = []
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

def delete_posts_from_group(personally_token, link):
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

def lock_all(links):
    from random_word import Words
    
    personally_token, _ = get_data()
    for link in links:
        global ex
        ex = Words()
        if not ex.status: 
            return 'Generate photos error'
        edit_group_info(personally_token,link)
        delete_photos_from_group(personally_token, link) 
        delete_posts_from_group(personally_token, link)
        #create_photos()
        if not main_photo(personally_token, link) or not back_photo(personally_token, link): 
            return 'Groups photo error'
    main_delete_messages()
    return 'All done!'   

def create_groups(captcha_sid = None, captcha_key = None):
    personally_token, user_id = get_data()
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

def post(group,captcha_sid = None, captcha_key = None):
    personally_token, user_id = get_data()
    captcha_sid = captcha_key = None
    text = 'Привет, если ты решил прикупить группу ВК, то ты пришел по адресу!\nВот то, что у нас есть в наличии на сегодня:\n'
    links = list(map(str, groups().keys()))
    subs = list(map(str, groups().values()))

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

def get_admins(group_id:int) -> list:
    '''
    This function collect all admins from your groups VK
    '''
    personally_token, user_id = get_data()

    response = requests.get('https://api.vk.com/method/groups.getMembers?',params={
        'access_token':personally_token,
        'group_id':group_id,
        'filter':'managers',
        'v':version
    }).json()['response']['items']

    admins = []
    for member in response:
        if member['role'] != 'creator':
            admins.append(member['id'])
    return admins

def kill_admin(group_id:int, user_id:int):
    'This function edit all admins and ban there'

    personally_token, _ = get_data()
    response = requests.get('https://api.vk.com/method/groups.editManager?',params={
        'access_token':personally_token,
        'group_id':group_id,
        'user_id':user_id,
        'role':'',
        'v':version
    }).json()['response']
    try:
        if response == 1: pass
    except:
        return 'Fail'
    response = requests.get('https://api.vk.com/method/groups.ban?',params={
        'access_token':personally_token,
        'group_id':group_id,
        'owner_id':user_id,
        'reason':'2',
        'v':version
    })
    try:
        if response == 1:
            return 'Successfull'
        else:
            return 'Fail'
    except:
        return 'Fail'

def main_admins():
    'This main function of collecting and killing admins'
    data = groups()
    for group_id in tqdm(data.keys()):
        admins = get_admins(group_id=group_id)
        for user_id in admins:
            kill_admin(group_id=group_id, user_id=user_id)

def get_messages(group_id):
    personally_token, _ = get_data()
    response = requests.get('https://api.vk.com/method/messages.getConversations',params={
        'access_token':personally_token,
        'count':200,
        'group_id':group_id,
        'v':version
    })
    data = [x['conversation']['peer']['id'] for x in response.json()['response']['items']]
    if response.json()['response']['count'] < 200:
        return data
    else:
        for offset in range(200,response.json()['response']['count'],200):
            response = requests.get('https://api.vk.com/method/messages.getConversations',params={
            'access_token':personally_token,
            'count':200,
            'offset':offset,
            'group_id':group_id,
            'v':version
            })
            data.extend([x['conversation']['peer']['id'] for x in response.json()['response']['items']])
        return data
        


def delete_messages(group_id, peer_id,*,captcha_key=None,captcha_sid=None):
    personally_token, _ = get_data()
    response = requests.get('https://api.vk.com/method/messages.deleteConversation',params={
        'access_token':personally_token,
        'peer_id':peer_id,
        'group_id':group_id,
        'v':version,
    })
    try:
        if response.json()['error']['error_code'] == 14:
            img_data = requests.get(response.json()['error']['captcha_img']).content
            with open('captcha_ms.jpeg', 'wb') as handler:
                handler.write(img_data)
            captcha_key = captcha_solved()
            captcha_sid = response.json()['error']['captcha_sid']
            delete_messages(group_id,peer_id,captcha_sid=captcha_sid,captcha_key=captcha_key)
        elif response.json()['error']['error_code'] == 9:
            time.sleep(5)
            delete_messages(group_id,peer_id)
    except: pass

def main_delete_messages():
    for gr in groups().keys():
        print(gr)
        data = get_messages(int(gr))
        print(len(data))
        for peer_id in data:
            delete_messages(gr, peer_id)

def set_group_links():
    personally_token, _ = get_data()
    captcha_key = captcha_sid = None
    session = requests.session()
    for gr in groups().keys():
        while True:
            response = session.get('https://api.vk.com/method/groups.edit?', params={
                'access_token': personally_token,
                'group_id':gr,
                'screen_name': randomword(10),
                'captcha_key':captcha_key,
                'captcha_sid':captcha_sid,
                'v':version
            })
        
            try:
                if response.json()['error']['error_code'] == 14:
                    img_data = requests.get(response.json()['error']['captcha_img']).content
                    with open('captcha_ms.jpeg', 'wb') as handler:
                        handler.write(img_data)
                    captcha_key = captcha_solved()
                    captcha_sid = response.json()['error']['captcha_sid']
                    
                elif response.json()['error']['error_code'] == 9:
                    time.sleep(5)
                
                elif response.json()['error']['error_code'] == 17:
                    break
                    validate = session.get(response.json()['error']['redirect_uri'])
                    soup = BeautifulSoup(validate.text, 'lxml')


                    hash = soup.find_all('a')[1]['href'].split('&')[1]
                    api_hash = soup.find_all('a')[1]['href'].split('&')[2].split('%')[-3]
                    1
                    
            except: break
        try:
            if response.json()['response'] == 1: 
                print(f'{gr} is complited')
        except: pass

if __name__ == "__main__":
    set_group_links()