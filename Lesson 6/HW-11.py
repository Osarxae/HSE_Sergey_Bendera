import requests
import json

class LegalAPI:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_data_from_efrsb(self, efrsb_id: int) -> dict:
        """
        Метод для получения данных из ЕФРСБ по идентификатору.

        :param efrsb_id: Идентификатор ЕФРСБ
        :return: Данные в формате JSON
        """
        url = f"https://legal-api.sirotinsky.com/api/v1/efrsb/{efrsb_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error getting data from EFRSB: {response.status_code}")

    def get_data_from_efrsb_by_inn(self, inn: str) -> dict:
        """
        Метод для получения данных из ЕФРСБ по ИНН.

        :param inn: ИНН
        :return: Данные в формате JSON
        """
        url = f"https://legal-api.sirotinsky.com/api/v1/efrsb/inn/{inn}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error getting data from EFRSB: {response.status_code}")

    def get_data_from_efrsb_by_ogrn(self, ogrn: str) -> dict:
        """
        Метод для получения данных из ЕФРСБ по ОГРН.

        :param ogrn: ОГРН
        :return: Данные в формате JSON
        """
        url = f"https://legal-api.sirotinsky.com/api/v1/efrsb/ogrn/{ogrn}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error getting data from EFRSB: {response.status_code}")

api = LegalAPI('4123saedfasedfsadf4324234f223ddf23')

efrsb_id = 123456  # Замените на правильный идентификатор ЕФРСБ
data = api.get_data_from_efrsb(efrsb_id)
print(json.dumps(data, indent=4))

inn = '1234567890'  # Замените на правильный ИНН
data = api.get_data_from_efrsb_by_inn(inn)
print(json.dumps(data, indent=4))

ogrn = '1234567890123'  # Замените на правильный ОГРН
data = api.get_data_from_efrsb_by_ogrn(ogrn)
print(json.dumps(data, indent=4))
