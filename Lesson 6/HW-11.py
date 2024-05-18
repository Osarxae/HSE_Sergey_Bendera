import requests
import json
from typing import Dict

class LegalAPI:

    BASE_URL = "https://api.sirotinsky.com"

    def __init__(self, token: str):
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
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
            return {}

    def get_organisation(self, efrsb_id: int) -> Dict:
        return self._get("efrsb/organisation", str(efrsb_id))

    def get_person(self, inn: str) -> Dict:
        return self._get("efrsb/person", inn)

    def get_trader(self, ogrn: str) -> Dict:
        return self._get("efrsb/trader", ogrn)

if __name__ == "__main__":

    api = LegalAPI('4123saedfasedfsadf4324234f223ddf23')

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
