import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import json
import pickle
import decimal
from datetime import datetime
from io import StringIO


class ParserCBRF:
    BASE_URL = "https://www.cbr.ru"
    DATA_URL = (
        f"{BASE_URL}/hd_base/mrrf/mrrf_7d/"
        "?UniDbQuery.Posted=True"
        "&UniDbQuery.From=05.1998"
        "&UniDbQuery.To=05.2024"
    )

    def __init__(self):
        self.data = None

    def fetch_and_parse_html(self):
        """Загрузка и парсинг HTML-страницы"""
        response = requests.get(self.DATA_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'data'})
        df = pd.read_html(StringIO(str(table)))[0]
        self.data = self.process_data(df)

    def process_data(self, df):
        """Обработка данных"""
        df.columns = [col.strip() for col in df.columns]
        try:
            df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')
        except ValueError:
            df['Дата'] = pd.to_datetime(df['Дата'])  # Попытка автоопределения формата даты

        for col in df.columns[1:]:
            df[col] = df[col].apply(lambda x: decimal.Decimal(str(x).replace(',', '.')) if pd.notnull(x) else None)
        return df

    def save_grouped_by_year(self, folder_path):
        """Сохранение данных, сгруппированных по годам"""
        if self.data is not None:
            grouped = self.data.groupby(self.data['Дата'].dt.year)
            for year, group in grouped:
                year_folder = folder_path / str(year)
                year_folder.mkdir(parents=True, exist_ok=True)
                self.save_to_formats(group, year_folder, year)

    def save_to_formats(self, data, folder, year):
        """Сохранение данных в разные форматы"""
        csv_path = folder / f'data_{year}.csv'
        json_path = folder / f'data_{year}.json'
        pickle_path = folder / f'data_{year}.pkl'

        data.to_csv(csv_path, index=False)

        data_dict = data.to_dict(orient='records')
        with open(json_path, 'w') as f:
            json.dump(data_dict, f, default=self.default)

        with open(pickle_path, 'wb') as f:
            pickle.dump(data, f)

    def load_from_pickle(self, filepath):
        """Загрузка данных из Pickle-файла"""
        with open(filepath, 'rb') as f:
            self.data = pickle.load(f)
        self.data = self.process_data(self.data)  # Применить обработку данных после загрузки

    def load_from_csv(self, filepath):
        """Загрузка данных из CSV-файла"""
        self.data = pd.read_csv(filepath)
        self.data = self.process_data(self.data)  # Применить обработку данных после загрузки

    @staticmethod
    def default(obj):
        if isinstance(obj, (datetime, decimal.Decimal)):
            return str(obj)
        raise TypeError(f"Object of type '{type(obj).__name__}' is not JSON serializable")

    def start(self):
        self.fetch_and_parse_html()
        folder_path = Path(__file__).parent / 'parsed_data'
        self.save_grouped_by_year(folder_path)


class DataManager:
    def __init__(self, data):
        self.data = data

    def get_by_date(self, date):
        """Получение данных по дате"""
        date = pd.to_datetime(date)
        return self.data[self.data['Дата'] == date]

    def get_latest(self):
        """Получение последних данных"""
        return self.data.iloc[-1]

    def get_average(self, col):
        """Получение среднего значения по колонке"""
        if col in self.data.columns:
            return self.data[col].mean()
        else:
            raise KeyError(f"Column '{col}' does not exist in data")

    def get_data_range(self, start_date, end_date):
        """Получение данных за диапазон дат"""
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        mask = (self.data['Дата'] >= start_date) & (self.data['Дата'] <= end_date)
        return self.data.loc[mask]


def main():
    parser = ParserCBRF()
    parser.start()

    folder_path = Path(__file__).parent / 'parsed_data'
    csv_path = folder_path / '2024' / 'data_2024.csv'
    pickle_path = folder_path / '2024' / 'data_2024.pkl'
    parser.load_from_csv(csv_path)
    parser.load_from_pickle(pickle_path)
    manager = DataManager(parser.data)

    print("Latest data entry:")
    print(manager.get_latest())

    example_date = '2024-05-10'
    print(f"\nData for {example_date}:")
    print(manager.get_by_date(example_date))

    column_name = 'Международные резервы'
    try:
        print(f"\nAverage value for column '{column_name}':")
        print(manager.get_average(column_name))
    except KeyError as e:
        print(e)

    start_date = '2023-01-01'
    end_date = '2023-12-31'
    print(f"\nData range from {start_date} to {end_date}:")
    print(manager.get_data_range(start_date, end_date))


if __name__ == "__main__":
    main()
