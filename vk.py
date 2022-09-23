import requests
from pprint import pprint
import time
from progress.bar import IncrementalBar
    
class VK:

    def __init__(self, vk_token, user_id, count, version='5.131'):
       self.token = vk_token
       self.id = user_id
       self.version = version
       self.count = count
    
    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'access_token': self.token,
                  'v': self.version,
                  'extended': '1',
                      'photo_sizes': '1',
                      'count': self.count,
                      'offset': 0
                      }
        res = (requests.get(url=url, params=params)).json()
        max_photos = []
        bar = IncrementalBar('Выгрузка с VK', max = len(res['response']['items']))
        for items in res['response']['items']:
            bar.next()
            time.sleep(1)
            like = str(items['likes']['count'])
            date = str(items['date'])
            max_photos.append({'file_name':(like +'_'+ date + '.jpg'), 'url':items['sizes'][-1]['url'], 'size':items['sizes'][-1]['type']})
        bar.finish()
        return max_photos