import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import DSN, password_4
from Models import create_table, Users_info, Black_list, White_list
import requests
from collections import OrderedDict
from pprint import pprint
import VK
import time
"""
код выполняет сортировку по запросу пользователя по параметрам ( город, пол, рамки возраста) из талбицы БД 
< Users_info > и возвращает отсортированные по запрошенным ползьзователям 3 самые лайкнутые фото со стены 
"""
engine = sqlalchemy.create_engine(DSN)

create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_photos(input_):
    time.sleep(0.33)
    photo_url = 'https://api.vk.com/method/photos.get'
    params = {'access_token': password_4, 'v': '5.131', 'owner_id': input_, 'album_id': 'wall', 'extended': 1}
    resp = requests.get(photo_url, params=params).json()
    resp = resp['response']['items']
    name_dict = []

    for item in resp:
        # print(item['sizes'])
        name_dict.append({})
        for i in item['sizes']:
            if i['type'] == 'y':
                name_dict[-1][i['url']] = item['likes']['count']



    sorted_pairs = sorted(((k, v) for d in name_dict for k, v in d.items()), key=lambda pair: pair[1], reverse=True)

    output = OrderedDict()
    for k, v in sorted_pairs:
        if k not in output:
            output[k] = v
            if len(output) == 3:
                break

    # pprint(sorted_pairs)
    pprint(output)



for c in session.query(Users_info).filter(Users_info.sex == 1, Users_info.city == 'Санкт-Петербург',Users_info.age >= 27, Users_info.age <= 35).all():
    users_id = c.__dict__['id']
    try:
        # print(users_id)
        get_photos(input_=users_id)
    except:
        pass



session.close()
