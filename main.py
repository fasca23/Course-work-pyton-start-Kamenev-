from pprint import pprint
from ya import YaDisk
from vk import VK
import requests
import time
from progress.bar import IncrementalBar
import os

def input_count():
    while True:
        count = input('\nВведите количество фотографий (только целое число от 1 до 10): ')
        if count.isdigit() and int(count)>0 and int(count)<=10:
            return count          

ya_token = ""

def input_token_vk():
    while True:
        token = input('\nВведите токен VK: ')
        if token != '':
            return token

vk_token = input_token_vk()

count = input_count()       

#При вводе 2 проверки: на отсутствие аккаунта и на отсутствие в нем фото.   
def input_id():
    id = input('\nВведите ID пользователя (только цифры): ')
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': id,
                'album_id': 'profile',
                'access_token': vk_token,
                'v': '5.131',
                'extended': '1',
                'photo_sizes': '1',
                'count': 1,
                'offset': 0
                }
    exam = requests.get(url=url, params=params).json()
    if 'error' in exam:
        print('Ошибка ввода')
    elif exam['response']['count']==0:
        print('В профиле нет картинок')
    return id

user_id = input_id()

if __name__ == '__main__':
    vk = VK(vk_token=vk_token, user_id=user_id, count=count)
    ya = YaDisk(token=ya_token)

bar = IncrementalBar('Загрузка на Яндекс Диск', max = len(vk.get_photos()))
for photo in vk.get_photos():
    bar.next()
    time.sleep(1)
    photo_url = photo['url']
    photo_name = photo['file_name']
    with open(photo_name, 'wb') as file:
        img = requests.get(photo_url)
        file.write(img.content)
    ya.upload_file_to_disk('test/'+ photo_name, photo_name)
    os.remove(photo_name)
bar.finish()
with open('list_images.txt', 'w', encoding='utf-8') as w:
    w.writelines(str(vk.get_photos()))