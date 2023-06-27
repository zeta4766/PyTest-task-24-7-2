from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

"""Позитивные тесты"""


# Получение api_key
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, api_key = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in api_key


# получение списка питомцев: всех или своих по фильтру my_pets
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


# Добавление питомца с фото
def test_add_new_pet_with_valid_data(name='Stitch', animal_type='experimen626', age=0, photo='images/pet_photo.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(name, animal_type, age, auth_key, photo)
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == str(age)


# Добавление питомца без фото
def test_add_new_pet_without_photo_valid_data(name='Ruben', animal_type='experiment 625', age=1):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(name, animal_type, age, auth_key)
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == str(age)


# Добавление фото последнему питомцу
def test_add_photo_valid_data(photo='images/ruben.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(result) > 0:
        pet_id = result['pets'][0]['id']
        pet_photo = result['pets'][0]['pet_photo']
        status, res = pf.add_photo(pet_id, photo, auth_key)
        assert status == 200
    else:
        assert False


# Изменение информации о последнем добавленном питомце
def test_update_pet_with_valid_data(name='Пчелобык', animal_type='Ушастый', age=89):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(result) > 0:
        pet_id = result['pets'][0]['id']
        status, res = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert res['name'] == name and res['animal_type'] == animal_type and res['age'] == str(age)
    else:
        assert False


# Удаление последнего добавленного питомца
def test_delete_pet_with_valid_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(result) > 0:
        pet_id = result['pets'][0]['id']
        status = pf.delete_pet(auth_key, pet_id)
        assert status == 200
        _, res = pf.get_list_of_pets(auth_key, 'my_pets')
        if len(res) > 0:
            assert res['pets'][0]['id'] != pet_id
    else:
        assert False


'''Негативные тесты'''


# Получение api_key с невалидным email
def test_get_api_key_for_invalid_email(email='not_valid_email', password=valid_password):
    status, api_key = pf.get_api_key(email, password)
    assert status == 403


# Получение api_key с невалидным password
def test_get_api_key_for_invalid_password(email=valid_email, password='not_valid_password'):
    status, api_key = pf.get_api_key(email, password)
    assert status == 403


# получение списка питомцев с невалидным api_key
def test_get_all_pets_with_invalid_key(filter=''):
    status, result = pf.get_list_of_pets({'key': 'aaa'}, filter)
    assert status == 403


# Добавление питомца с фото невалидные данные
def test_add_new_pet_with_invalid_data(name='', animal_type='', age={}, photo='images/rrr.txt'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(name, animal_type, age, auth_key, photo)
    assert status == 400


# Изменение информации, невалидный pet_id
def test_update_pet_with_invalid_data(name='Пчелобык', animal_type='Ушастый', age=89, pet_id='-13'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, res = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 400

# Удаление питомца, невалидный pet_id, возвращает 200, а в документации не написано, что должно быть
def test_delete_pet_with_valid_id(pet_id='-13'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status = pf.delete_pet(auth_key, pet_id)
    assert status == 400
