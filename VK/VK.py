import requests
import time
from sqlalchemy import create_engine
from config import password_4, my_id
import re
import pandas as pd
from config import DSN
'''
Модуль запрашивает у АПИ ВК списки пользователей в сообществах знакомств и добавляет их по заданным критериям
в БД POstgresql на локальном хосте. Для использования нужны свой id-ВК, ВК=токенб,  DSN типа 
DSN = 'postgresql+psycopg2://< аккаунт >: < пароль >@localhost:5432/< название БД >'
Для увеличения кол-ва запрашиваемых сообществ  увеличить параметр < count > в вызове < vk.get_users_id(q='знакомств',
count=5) > для увеличения лимита запрашиваемых пользователей сообщества в функции < users_info >
 увеличить параметр < quantity >
'''

class VK:
    url = 'https://api.vk.com/method/'
    users_id = []
    user_data = []

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def search_groups(self, q, count, sorting=6):
        params = {'q': q, 'access_token': self.token, 'sort': sorting, 'v': self.version, 'count': count,
                  'country_id': 1}
        url = 'https://api.vk.com/method/groups.search'
        req = requests.get(url, params={**self.params, **params}).json()
        req = req['response']['items']
        target_req = ','.join([str(group['id']) for group in req])

        return target_req

    def get_users_id(self, q, count):
        for id_group in self.search_groups(q, count):
            params = {'access_token': self.token, 'v': self.version, 'group_id': id_group}
            url = 'https://api.vk.com/method/groups.getMembers'
            resp = requests.get(url, params={**self.params, **params}).json()
            req1 = resp['response']['items']
            self.users_id = req1
            return self.users_id

    def users_info(self):
        quantity = 0
        for user_inf in self.users_id:
            if quantity != 60:
                quantity += 1
                time.sleep(0.33)
                url = 'https://api.vk.com/method/users.get'
                params = {'user_ids': user_inf, 'fields': 'bdate, sex, city'}
                response = requests.get(url, params={**self.params, **params}).json()
                try:
                    res1 = response['response'][0]

                    if 'city' in res1.keys() and re.match(r"\d+\.\d+\.\d+", res1['bdate']):
                        self.user_data.append({})
                        self.user_data[-1]['id'] = res1['id']
                        self.user_data[-1]['first_name'] = res1['first_name']
                        self.user_data[-1]['second_name'] = res1['last_name']
                        self.user_data[-1]['birth_date'] = res1['bdate']
                        self.user_data[-1]['city'] = res1['city']['title']
                        self.user_data[-1]['sex'] = res1['sex']
                    else:
                        pass

                except:
                    pass
            else:
                break

        return self.user_data

class DB:
    def __init__(self, dsn):
        self.dsn = dsn
    def create_conn(self, data):
        conn = create_engine(self.dsn)

        for line in data:
            try:
                df = pd.DataFrame(line, index=[0])
                print(df)
                df.to_sql('users_info', conn, if_exists='append', index=False)
            except:
                pass


if __name__ == '__main__':
    access_token = password_4
    user_id = my_id
    vk = VK(access_token, user_id)
    vk.get_users_id(q='знакомств', count=5)
    vk.users_info()
    db = DB(DSN)
    db.create_conn(vk.user_data)




