import requests
import random
import shutil
from PIL import Image
import os

class Words:
    def __init__(self):
        self.words = self.collect_words()
        self.word = random.choice(self.words)
        self.__api_key = 'ICnN1L3R37b2fayZKfh2+g==VkPrI8dzevNe58KC'
        self.generate_picture_status = self.generate_picture()

        self.width_avatar = 500
        self.lenght_avatar = 500
        self.width_poster = 1590
        self.lenght_poster = 530

        self.resize_status_avatar = self.resize(self.width_avatar, self.lenght_avatar,'_avatar')
        self.resize_status_poster = self.resize(self.width_poster, self.lenght_poster,'_poster')

        self.status = self.status_checker()

    def status_checker(self):
        if self.resize_status_avatar and self.resize_status_poster and self.generate_picture_status:
            return True
        else: False

    def collect_words(self):
        words = []
        headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.931 YaBrowser/23.9.0.0 Safari/537.36',
        }
        response = requests.get('https://randomwordgenerator.com/json/words_ws.json', headers=headers).json()['data']
        for x in range(len(response)):
            words.append(response[x]['word']['value'])
        return words

    def generate_picture(self): 
        category = 'nature'
        api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
        response = requests.get(api_url, headers={'X-Api-Key': self.__api_key, 'Accept': 'image/jpg'}, stream=True)
        if response.status_code == requests.codes.ok:
            if not os.path.isdir("photos"): os.mkdir('photos')
            with open(f'photos/image.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            return True
        else:
            print("Error:", response.status_code, response.text)
            return False
    
    def resize(self, width, lenght, postfix = ''):
        try:
            path = f'photos/image.jpg'
            photo = Image.open(path)
            new_photo = photo.resize((width, lenght))
            new_photo.save(f'photos/image{postfix}.jpg')
            return True
        except Exception as e:
            print(e)
            return False
        
if __name__ == "__main__":
    a = Words()
    print(a.word)
