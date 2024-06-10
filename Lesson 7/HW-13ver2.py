import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import pickle


class ParserCBRF:
    def __init__(self):
        self.data = {}

    @staticmethod
    def __parse_html(url):
        """Загрузка и парсинг HTML-страницы"""
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешный статус ответа
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

    def start(self):
        """Запуск парсинга"""
        url = "https://www.cbr.ru/currency_base/daily/"
        self.data = self.__parse_html(url)
        return self.data

    def save_to_json(self, file_path):
        """Сохранение данных в JSON-файл"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False, sort_keys=True)
        print(f"Данные сохранены в {file_path}")

    def save_to_pickle(self, file_path):
        """Сохранение данных в Pickle-файл"""
        with open(file_path, 'wb') as f:
            pickle.dump(self.data, f)
        print(f"Данные сохранены в {file_path}")

    def load_from_pickle(self, file_path):
        """Загрузка данных из Pickle-файла"""
        with open(file_path, 'rb') as f:
            self.data = pickle.load(f)
        print(f"Данные загружены из {file_path}")
        return self.data


def main():
    parser = ParserCBRF()
    try:
        data = parser.start()
        if data:
            json_file_path = f"CBRF_{datetime.now().strftime('%Y-%m-%d')}.json"
            pickle_file_path = f"CBRF_{datetime.now().strftime('%Y-%m-%d')}.pkl"
            parser.save_to_json(json_file_path)
            parser.save_to_pickle(pickle_file_path)
        else:
            print("Не удалось получить данные.")
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при загрузке данных: {e}")


if __name__ == '__main__':
    main()
