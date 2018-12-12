import requests
import time
import json
from pprint import pprint

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'


class User:
    # def __init__(self, id_user):
    #     self.id_user = id_user

    def utils_resolveScreenName(self, screen_name):
        params = {
            'screen_name': screen_name,
            'access_token': token,
            'v': '5.92'
        }

        response = requests.get('https://api.vk.com/method/utils.resolveScreenName',
                                params)
        print('.')
        return response.json()

    def get_groups(self):  # группы пользователя
        params = {
            'user_id': user_id,
            'extended': 1,
            'fields': 'members_count',
            'access_token': token,
            'v': '5.92'
        }

        response = requests.get('https://api.vk.com/method/groups.get',
                                params)
        print('.')
        return response.json()

    def get_friends(self):  # друзья пользователя
        params = {
            'user_id': user_id,
            'access_token': token,
            'v': '5.92'
        }

        response = requests.get('https://api.vk.com/method/friends.get',
                                params)
        print('.')
        return response.json()

    def id_groups(self):  # id групп пользователя
        id_groups = []
        for i in user.get_groups()['response']['items']:
            id_groups.append(i['id'])
        return id_groups

    def groups_isMember(self, group_id, user_ids):  # является ли пользователь участником сообществ 1 это да

        params = {
            'group_id': group_id,
            'user_ids': user_ids,
            'access_token': token,
            'v': '5.92'
        }
        response = requests.get('https://api.vk.com/method/groups.isMember',
                                params)
        print('.')
        return response.json()

    def groups_getById(self, group_id):  # Инфа о сообществе

        params = {
            'group_ids': group_id,
            'fields': 'members_count',
            'access_token': token,
            'v': '5.92'
        }
        response = requests.get('https://api.vk.com/method/groups.getById',
                                params)
        print('.')
        return response.json()

    def id_unique_groups(self):
        try:
            id_groups_user = user.id_groups()  # id групп пользователя
            unique_groups = []
            for i in id_groups_user:
                if user.groups_isMember(i, user.get_friends()) == {'response': 0}:
                    unique_groups.append(i)
            return unique_groups
        except KeyError:
            print("Пользователь закрыл доступ к группам:(")
            raise SystemExit

user = User()
name_user = 'yashafat' # ВВОД КОРОТКОГО ИМЕНИ ИЛИ ID!!!!
try:
    user_id = User().utils_resolveScreenName(name_user)['response']['object_id']  # Kris(120597952) me 112336927
except TypeError:
    user_id = name_user
final_list = []
for i in user.id_unique_groups():
    user.groups_getById(i)
    try:
        for a in user.groups_getById(i)['response']:
            json_group = {
                'name': a['name'],
                'gid': a['id'],
                'members_count': a['members_count']
            }
            final_list.append(json_group)
    except KeyError:
        time.sleep(1)

with open("newsafr2.json", "w", encoding='utf_8_sig') as datafile:
    json.dump(final_list, datafile, ensure_ascii=False)
pprint(final_list)
