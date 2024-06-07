import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


class ParserCBRF:

    def __init__(self):
        self.data = {}

    def __download_file(self, url, file_type):
        """Загрузка файла с указанного URL"""
        response = requests.get(url)
        if response.status_code == 200:
            file_path = f"CBRF_{datetime.now().strftime('%Y-%m-%d')}.{file_type}"
            with open(file_path, 'w') as f:
                if file_type == 'json':
                    data = self.__parse_html(url)
                    json.dump(data, f, indent=4)
                else:
                    f.write(response.content)
            return file_path
        else:
            return None

    def __parse_html(self, url):
        """Парсинг HTML-страницы"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'data'})
        data = {"Price": []}
        if table:
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) > 1:
                    rate = cols[1].text.strip()
                    sell = cols[4].text.strip()
                    data["Price"].append({"Currency name": rate, "sell": sell})
        return data

    def __parse_json(self, file_path):
        """Парсинг JSON-файла"""
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.data.update(data)

    def start(self):
        """Запуск парсинга"""
        url = "https://www.cbr.ru/currency_base/daily/"
        file_path = self.__download_file(url, 'json')
        if file_path:
            self.__parse_json(file_path)
        else:
            self.__parse_html(url)
        return self.data


def main():
    parser = ParserCBRF()
    parser.start()


if __name__ == '__main__':
    main()


