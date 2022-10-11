from vk_bot.VK_app import VK
import json
from vk_api.longpoll import VkEventType
from vk_bot.keys import send_kb, send_kb_in_message
import config

vkapp = VK(token_user=config.vk_token_user, token_group=config.vk_token_group)

if __name__ == '__main__':
    # def create_file(total_dict):
    #     with open(f"total.json", "w",encoding='UTF-8') as write_file:
    #         json.dump(total_dict, write_file)
    #     print(f'Создан файл: total.json')
    for event in vkapp.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                user_id = event.user_id
                send_kb(user_id, msg.lower())
                if msg == 'hi':
                    vkapp.send_message('hallo', user_id)
                    vkapp.send_message('wazzup man?', user_id)
                if msg == 'ok':
                    vkapp.send_message('nice', user_id)
                if msg == 'name':
                    vkapp.send_message(vkapp.get_name(user_id), user_id)
                if msg == 'age':
                    vkapp.send_message(vkapp.get_age(user_id), user_id)
                if msg == 'city':
                    vkapp.send_message(vkapp.get_city_id(user_id), user_id)
                if msg == 'sex':
                    vkapp.send_message(vkapp.get_reverse_sex(user_id), user_id)
                if msg == 'search':
                    total_dict = vkapp.total_dict(user_id)
                    vkapp.send_message(f'https://vk.com/id{(list(total_dict)[0])}', user_id)
                    send_kb_in_message(user_id, msg.lower(), (list(total_dict)[0]))
                    vkapp.send_foto(user_id=user_id, user_id_foto=(list(total_dict)[0]))
                    print(total_dict)
                    # create_file(total_dict)
