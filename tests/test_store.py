import allure
import requests
import pytest
import jsonschema
from .schemas.store_schema import STORE_SCHEMA
BASE_URL = "http://5.181.109.28:9090/api/v3"
@allure.feature("Store")
class TestStore:
    @allure.title("Размещение нового заказа")
    def test_add_new_store(self, create_store):
        with allure.step("Получить id созданного заказа"):
            store_id = create_store["id"]

        with allure.step("Получение информации о заказе по id"):
            response = requests.get(url=f"{BASE_URL}/store/order/{store_id}")
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200,"Код ответа не совпал с ожидаемым"

        with allure.step("Проверка соответствия JSON схеме"):
            jsonschema.validate(instance=response_json, schema=STORE_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json["id"] == 1, "id заказа не совпадает с ожидаемым"
            assert response_json["petId"] == 1, "id питомца не совпадает с ожидаемым"
            assert response_json["quantity"] == 1, "количество  не совпадает в заказе с ожидаемым"
            assert response_json["status"] == "placed", "статус заказа не совпадает с ожидаемым"
            assert response_json["complete"] == True, "значение поля 'complete' не совпадает с ожидаемым"


    @allure.title("Получение информации о заказе по ID")
    def test_get_store_by_id(self,  create_store):
        with allure.step("Получить id созданного заказа"):
            store_id = create_store["id"]

        with allure.step("Отправка запроса на получение заказа по id"):
            response = requests.get(f"{BASE_URL}/store/order/{store_id}")


        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == 200,"Код ответа не совпал с ожидаемым"
            assert isinstance(response.json(),dict)

        response_data = response.json()

        with allure.step("Проверка тела ответа"):
            assert response_data["id"] == 1,"ID заказа не совпадает с ожидаемым."
            assert response_data["petId"] == 1, "В ответе отсутствует поле petId"
            assert response_data["quantity"] == 1, "В ответе отсутствует поле quantity"
            assert response_data["status"] == "placed", "В ответе отсутствует поле status"
            assert response_data["complete"] == True, "В ответе отсутствует поле complete"

    @allure.title("Удаление заказа по ID")
    def test_delete_store(self, create_store):
        with allure.step("Получить id созданного заказа"):
            storeId = create_store["id"]

        with allure.step("Получение информации о заказе по id"):
            response = requests.get(url=f"{BASE_URL}/store/order/{storeId}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на удаление заказа по id"):
            delete_store = requests.delete(f"{BASE_URL}/store/order/{storeId}")


        with allure.step("Проверка статуса ответа после удаления"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка статуса ответа после повторного запроса заказа по id"):
            check_response = requests.get(f"{BASE_URL}/store/order/{storeId}")
            assert check_response.status_code == 404, "Заказ все еще существует"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_store(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение информации об инвентаре по статусам")
    @pytest.mark.parametrize(
        "status_inventory, expected_quantity",
        [
            ("approved", 57),
            ("delivered", 50)
        ]
    )
    def test_get_inventory_by_status(self, status_inventory, expected_quantity):
        with allure.step(f"Отправка запроса на получение инвентаря по статусам {status_inventory}"):
            response = requests.get(f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка формата данных"):
            inventory = response.json()
            assert isinstance(response.json(), dict)

        with allure.step(f"Проверка количества инвентаря со статусом {status_inventory}"):
            assert status_inventory in inventory, "Статус отсутствует в ответе"
            assert inventory[status_inventory] == expected_quantity, "Количество инвентаря не совпадает с ожидаемым"
