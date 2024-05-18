import requests
import json
from typing import Dict

class LegalAPI:

    BASE_URL = "https://api.sirotinsky.com"

    def __init__(self, token: str):
        if not token or len(token) != 32:
            raise ValueError("Некорректный токен")
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _get(self, endpoint: str, id: str) -> Dict:
        url = f"{self.BASE_URL}/{endpoint}/{id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
            return {}

    def get_organisation(self, efrsb_id: int) -> Dict:
        if not efrsb_id or not isinstance(efrsb_id, int):
            raise ValueError("Некорректный идентификатор ЕФРСБ")
        return self._get("efrsb/organisation", str(efrsb_id))

    def get_person(self, inn: str) -> Dict:
        if not inn or len(inn) != 12:
            raise ValueError("Некорректный ИНН")
        return self._get("efrsb/person", inn)

    def get_trader(self, ogrn: str) -> Dict:
        if not ogrn or len(ogrn) != 13:
            raise ValueError("Некорректный ОГРН")
        return self._get("efrsb/trader", ogrn)

if __name__ == "__main__":

    api = LegalAPI('4123saedfasedfsadf4324234f223ddf23')

    try:
        organisation_id = 123456  # Замените на правильный идентификатор ЕФРСБ
        data = api.get_organisation(organisation_id)
        if data:
            print(json.dumps(data, indent=4))

        inn = '1234567890'  # Замените на правильный ИНН
        data = api.get_person(inn)
        if data:
            print(json.dumps(data, indent=4))

        ogrn = '1234567890123'  # Замените на правильный ОГРН
        data = api.get_trader(ogrn)
        if data:
            print(json.dumps(data, indent=4))
    except ValueError as e:
        print(f"Ошибка: {e}")


