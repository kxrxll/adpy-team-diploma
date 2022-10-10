import requests
from vk_api.longpoll import VkLongPoll
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import time
from datetime import datetime


class VK:

    def __init__(self, token_user, token_group, version='5.131'):
        self.token_user = token_user
        self.token_group = token_group
        self.version = version
        self.params_group = {'access_token': self.token_group, 'v': self.version}
        self.params_user = {'access_token': self.token_user, 'v': self.version}
        self.vk = vk_api.VkApi(token=token_group)
        self.vk_session = vk_api.VkApi(token=token_group)
        self.session_api = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk)
        self.users_dict = {}
        """начальная клавиатура"""
        self.key_start = VkKeyboard(one_time=True)
        self.key_start.add_button(label='Start', color=VkKeyboardColor.PRIMARY)
        """постоянная клавиатура"""
        self.key_const = VkKeyboard(one_time=False)
        self.key_const.add_button(label='previous', color=VkKeyboardColor.PRIMARY)
        self.key_const.add_button(label='to black', color=VkKeyboardColor.NEGATIVE)
        self.key_const.add_button(label='to white', color=VkKeyboardColor.POSITIVE)
        self.key_const.add_button(label='next', color=VkKeyboardColor.PRIMARY)
        self.key_const.add_line()
        self.key_const.add_button(label='black_show', color=VkKeyboardColor.PRIMARY)
        self.key_const.add_button(label='white_show', color=VkKeyboardColor.PRIMARY)

    def send_message(self, message, user_id, attachment=None, keyboard=None):
        self.vk_session.method("messages.send", {"user_id": user_id,
                                                 "message": message,
                                                 "random_id": 0,
                                                 'keyboard': keyboard,
                                                 'attachment': attachment})

    """кнопка старт"""

    def start(self, user_id, message):
        self.send_message(user_id=user_id, message=message, keyboard=self.key_start.get_keyboard())

    """кнопка после старта"""

    def post_start(self, user_id, message):
        self.send_message(user_id=user_id, message=message, keyboard=self.key_const.get_keyboard())

    """кнопка удаления из любимых"""

    def delete_favourite(self, user_id, message, vk_id):
        key_tempo = VkKeyboard(inline=True)
        key_tempo.add_button(label=f'Delete favourite_{vk_id}', color=VkKeyboardColor.NEGATIVE)
        self.send_message(user_id=user_id, message=message, keyboard=self.key_tempo.get_keyboard())

    def delete_unfavourite(self, user_id, message, vk_id):
        """кнопка удаления из нелюбимых"""
        key_tempo = VkKeyboard(inline=True)
        key_tempo.add_button(label=f'Delete unfavourite_{vk_id}', color=VkKeyboardColor.NEGATIVE)
        self.send_message(user_id=user_id, message=message, keyboard=self.key_tempo.get_keyboard())

    def user_info(self, user_id):
        res = self.users_dict.get(user_id)
        if res is None:
            url = 'https://api.vk.com/method/users.get'
            params = {'user_ids': user_id, 'fields': 'city, sex, bdate, photo_id'}
            res = requests.get(url, params={**self.params_group, **params}).json()
            self.users_dict.clear()
            self.users_dict[user_id] = res
        return res

    def get_name(self, user_id):
        """chat user name request"""
        res = self.user_info(user_id)
        try:
            return res['response'][0]['first_name']
        except KeyError:
            self.send_message(user_id, 'token input mistake')

    def get_surname(self, user_id):
        """chat user surname request"""
        res = self.user_info(user_id)
        try:
            return res['response'][0]['last_name']
        except KeyError:
            self.send_message(user_id, 'token input mistake')

    def get_age(self, user_id):
        """chat user age request"""
        res = self.user_info(user_id)
        date = res['response'][0].get('bdate')
        if (date is not None) and (len(date.split('.'))) == 3:
            year = datetime.now().year
            print(date)
            return year - datetime.strptime(date, '%d.%m.%Y').year
        else:
            self.send_message(user_id, 'what is your age:  ')
            for event in self.longpoll.listen():
                if event.to_me:
                    age = event.text.lower()
                    try:
                        a = int(age)
                    except:
                        return 35
                    if (a > 65) or (a < 16):
                        return 35
                    else:
                        return a

    def get_primary_foto_id(self, user_id):
        """chat user main photo request"""
        res = self.user_info(user_id)
        try:
            foto = res['response'][0]['photo_id']
            return foto.split(sep='_')[1]
        except KeyError:
            self.send_message(user_id, 'token input mistake')

    def get_city_id(self, user_id):
        res = self.user_info(user_id)
        try:
            return res['response'][0]['city']['id']
        except KeyError:
            return None

    def get_reverse_sex(self, user_id):
        """chat user hooker sex"""
        res = self.user_info(user_id)
        try:
            sex = res['response'][0]['sex']
        except KeyError:
            self.send_message(user_id, 'token input mistake')
        if sex == 1:
            return 2
        elif sex == 2:
            return 1
        else:
            return 0

    def get_sex(self, user_id):
        """chat user sex request"""
        res = self.user_info(user_id)
        try:
            return res['response'][0]['sex']
        except KeyError:
            self.send_message(user_id, 'token input mistake')

    def user_foto(self, user_id, album='profile', offset=0):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id, 'album_id': album, 'extended': '1', 'photo_sizes': '1', 'offset': offset}
        res = requests.get(url, params={**self.params_user, **params})
        time.sleep(0.4)
        return res.json()

    def foto_dict(self, user_id, list_album='profile'):
        dict_foto = {}
        print(f'searching photos {user_id}')
        album = list_album
        offset = 0
        while True:
            user_foto = self.user_foto(user_id, album, offset)
            for item in (user_foto['response']['items']):
                like = item['likes']['count']
                dict_foto[like] = f"{user_id}_{item['id']}"
            offset += len(user_foto['response']['items'])
            if offset >= user_foto['response']['count']:
                break
        sort_key = sorted(dict_foto, reverse=True)
        sort_dict = {x: dict_foto[x] for x in sort_key}
        while len(sort_dict) > 3:
            sort_dict.popitem()
        return sort_dict

    def total_dict(self, user_id):
        dict_total = {}
        response = self.search_user(user_id)
        if response.get('response') is not None:
            print(len(response['response']['items']))
            for user_search in response['response']['items']:
                if (user_search['is_closed'] == False) and (user_search.get('bdate') is not None):
                    if len(user_search.get('bdate').split('.')) > 2:
                        city_title = None
                        if user_search.get('city') is not None:
                            city_title = user_search['city']['title']
                        dict_total[user_search['id']] = {
                            'first_name': user_search['first_name'],
                            'last_name': user_search['last_name'],
                            'sex': user_search['sex'],
                            'age': datetime.now().year - datetime.strptime(user_search['bdate'], '%d.%m.%Y').year,
                            'city': city_title
                        }
            return dict_total

    def search_user(self, user_id, down_age=1, up_age=1, count=1000):
        """searching of user"""
        age = self.get_age(user_id)
        url = f'https://api.vk.com/method/users.search'
        params = {
            'sex': self.get_reverse_sex(user_id),
            'age_from': age - down_age,
            'age_to': age + up_age,
            'city': self.get_city_id(user_id),
            'status': '1' or '6',
            'has_photo': '1',
            'sort': '0',
            'fields': 'is_closed, id, first_name, last_name, city, bdate, sex',
            'count': count
        }
        res = requests.get(url, params={**self.params_user, **params}).json()
        return res

    def send_foto(self, user_id, user_id_foto, message=''):
        photos = ''
        for key, value in self.foto_dict(user_id_foto).items():
            photos += f'photo{value},'
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'attachment': f'{photos}',
                                         'random_id': 0})
