import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(level=logging.INFO)


class ParserCBRF:
    """Парсер данных с сайта ЦБ РФ"""

    def __init__(self):
        self.data = {}
        self.url = "https://www.cbr.ru/currency_base/daily/"
        self.file_path = f"CBRF_{datetime.now().strftime('%Y-%m-%d')}.json"

    def download_file(self) -> str:
        """Загрузка файла с указанного URL"""
        response = requests.get(self.url)
        if response.status_code == 200:
            with open(self.file_path, 'w') as file:
                json.dump(self.parse_html(self.url), file, indent=4)
            return self.file_path
        else:
            logging.error(f"Ошибка загрузки файла: {response.status_code}")
            return None

    def parse_html(self, url: str) -> dict:
        """Парсинг HTML-страницы"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'data'})
        data = {"Price": []}
        if table:
            data["Price"] = [
                {"Currency name": row.find_all('td')[1].text.strip(), "sell": row.find_all('td')[4].text.strip()} for
                row in table.find_all('tr')[1:]]
        return data

    def parse_json(self, file_path: str) -> None:
        """Парсинг JSON-файла"""
        with open(file_path, 'r') as file:
            self.data.update(json.load(file))

    def start(self) -> dict:
        """Запуск парсинга"""
        file_path = self.download_file()
        if file_path:
            self.parse_json(file_path)
        else:
            self.data = self.parse_html(self.url)
        return self.data


def main():
    parser = ParserCBRF()
    parser.start()


if __name__ == '__main__':
    main()
