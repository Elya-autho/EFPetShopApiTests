import allure
import requests
import pytest
import jsonschema
from .schemas.pet_schema import PET_SCHEMA
BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code==200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text=="Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
           payload = {"id": 9999,
                    "name": "Non-existent Pet",
                    "status": "available"
                    }
           response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {"id": 1,
                       "name": "Buddy",
                       "status": "available"
                       }
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "имя питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_new_pet(self):
        with allure.step("Подготовка данных для создания питомца с полными данными"):
            payload = {"id": 100,
                       "name": "doggie",
                       "category": {
                           "id": 1,
                            "name": "Dogs"
                       },
                       "photoUrls": ["https://storage-api.petstory.ru/resize/1000x1000x80/cb/48/7f/cb487f4677a640329e92ac0076004607.jpeg"],
                       "tags": [{
                           "id":1,
                            "name": "friendly"
                       }],
                       "status": "available"
            }
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            # assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            # assert response_json["name"] == payload["name"], "имя питомца не совпадает с ожидаемым"
            # assert response_json["category"]["id"] == payload["category"]["id"], "id категории питомца не совпадает с ожидаемым"
            # assert response_json["category"]["name"] == payload["category"]["name"], "имя категории питомца не совпадает с ожидаемым"
            # assert response_json["photoUrls"] == payload["photoUrls"], "photoUrls питомца не совпадает с ожидаемым"
            # assert response_json["tags"][0]["id"] == payload["tags"][0]["id"], "id тэга питомца не совпадает с ожидаемым"
            # assert response_json["tags"][0]["name"] == payload["tags"][0]["name"], "имя тэга питомца не совпадает с ожидаемым"
            # assert response_json["status"] == payload["status"], "статус питомца не совпадает с ожидаемым"

    @allure.title("Обновление информации о питомце")
    def test_update_information_pet(self,create_pet):
        with allure.step("Получить id созданного питомца"):
            petId=create_pet["id"]

        with allure.step("Получение информации о питомце по id"):
            response = requests.get(url=f"{BASE_URL}/pet/{petId}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на обновление информации о питомце"):
                payload = {"id": petId,
                           "name": "Buddy Updated",
                           "status": "sold"
                           }
                response = requests.put(url=f"{BASE_URL}/pet",json=payload)
                update_pet=requests.get(f"{BASE_URL}/pet/{petId}").json()

        with allure.step("Проверка статуса ответа после обновления"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка обновления данных о питомце"):
            assert update_pet["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert update_pet["name"] == payload["name"], "имя питомца не совпадает с ожидаемым"
            assert update_pet["status"] == payload["status"], "статус питомца не совпадает с ожидаемым"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet(self, create_pet):
        with allure.step("Получить id созданного питомца"):
            petId = create_pet["id"]

        with allure.step("Получение информации о питомце по id"):
            response = requests.get(url=f"{BASE_URL}/pet/{petId}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на удаление питомца по id"):
            delete_pet = requests.delete(f"{BASE_URL}/pet/{petId}")


        with allure.step("Проверка статуса ответа после удаления"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка статуса ответа после повторного запроса питомца по id"):
            check_response = requests.get(f"{BASE_URL}/pet/{petId}")
            assert check_response.status_code == 404, "Питомец все еще существует"


    @allure.title("Получение списка питомцев по валидному статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold",200),

        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            assert isinstance(response.json(),list)

    @allure.title("Получение списка питомцев по не валидному статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("stock", 400),
            ("", 400)

        ]
    )
    def test_get_pets_by_invalid_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по не валидному статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            assert isinstance(response.json(), dict)




