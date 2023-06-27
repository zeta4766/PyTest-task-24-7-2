import json

import requests
import settings


class PetFriends:
    '''апи библиотека к веб приложению Pet Friends'''

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str):
        '''Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключом пользователя, найденного по указанным email и password'''

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        try:
            api_key = res.json()
        except:
            api_key = res.text
        return status, api_key

    def get_list_of_pets(self, auth_key: json, filter: str):
        '''Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо "my_pets" - получить список
        собственных питомцев'''

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + "api/pets", headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, name: str, animal_type: str, age: int, auth_key: json, pet_photo: str):
        '''Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца'''
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_pet_without_photo(self, name: str, animal_type: str, age: int, auth_key: json):
        '''Метод отправляет (постит) на сервер данные о добавляемом питомце без фото и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца'''
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo(self, pet_id: str, pet_photo: str, auth_key: json):
        '''Метод отправляет (постит) на сервер фото питомца по известному id питомца и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца'''
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, files=file)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str):
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        return status

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int):
        '''Метод отправляет запрос на сервер о обновлении данных питомца по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца'''

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
