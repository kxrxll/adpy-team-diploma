import sqlalchemy
from sqlalchemy.orm import sessionmaker
from config import DSN, password_4
from Models import create_table, Users_info, Black_list, White_list
import requests
from collections import OrderedDict
import time

create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()
password = config["VK"]["token"]

def get_photos(input_):
    time.sleep(0.33)
    photo_url = 'https://api.vk.com/method/photos.get'
    params = {'access_token': password, 'v': '5.131', 'owner_id': input_, 'album_id': 'wall', 'extended': 1}
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


bl1 = Black_list(id_user=737786081, id_db_user=56)
wl = White_list(id_user=737786081, id_db_user=46)
# session.add_all([bl1,wl])
# session.commit()

id_black_list = []
for c in session.query(Black_list).all():
    id_black_list.append(c.__dict__['id_db_user'])

id_white_list = []
for c in session.query(White_list).all():
    id_white_list.append(c.__dict__['id_db_user'])

for c in session.query(Users_info).filter(Users_info.sex == 2, Users_info.city == 'Москва', Users_info.age >= 27,
                                          Users_info.age <= 38).all():
    users_id = c.__dict__['id']
    try:
        if users_id in id_black_list:
            pass
        else:
            print(users_id)
            get_photos(input_=users_id)
    except:
        pass
        
session.close()
