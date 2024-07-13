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

    @staticmethod
    def process_data(df):
        """Статический метод для обработки данных"""
        df.columns = [col.strip() for col in df.columns]
        try:
            df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')
        except ValueError:
            df['Дата'] = pd.to_datetime(df['Дата'])

        for col in df.columns[1:]:
            df[col] = df[col].apply(
                lambda x: decimal.Decimal(str(x).replace(',', '.')) if pd.notnull(x) else None
            )
        return df

    def save_grouped_by_year(self, folder_path):
        """Сохранение данных, сгруппированных по годам"""
        if self.data is not None:
            grouped = self.data.groupby(self.data['Дата'].dt.year)
            for year, group in grouped:
                year_folder = folder_path / str(year)
                year_folder.mkdir(parents=True, exist_ok=True)
                ParserCBRF.save_to_formats(group, year_folder, year)

    @staticmethod
    def save_to_formats(data, folder, year):
        """Статический метод для сохранения данных в разные форматы"""
        csv_path = folder / f'data_{year}.csv'
        json_path = folder / f'data_{year}.json'
        pickle_path = folder / f'data_{year}.pkl'

        data.to_csv(csv_path, index=False)
        data['Дата'] = data['Дата'].dt.strftime('%Y-%m-%d')
        data_dict = data.to_dict(orient='records')

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=4, ensure_ascii=False, default=ParserCBRF.default)

        with open(pickle_path, 'wb') as f:
            pickle.dump(data, f)

    def load_all_data(self, folder_path):
        """Загрузка данных из всех файлов в указанной папке"""
        all_files = folder_path.glob('**/*.[cp][sv]*')
        data_frames = []

        for file in all_files:
            if file.suffix == '.csv':
                df = pd.read_csv(file)
                df = self.process_data(df)
                data_frames.append(df)
            elif file.suffix == '.pkl':
                with open(file, 'rb') as f:
                    df = pickle.load(f)
                    df = self.process_data(df)
                    data_frames.append(df)

        if data_frames:
            self.data = pd.concat(data_frames).drop_duplicates().reset_index(drop=True)

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
        start_date = pd.to_datetime(start_date, dayfirst=True)
        end_date = pd.to_datetime(end_date, dayfirst=True)
        mask = (self.data['Дата'] >= start_date) & (self.data['Дата'] <= end_date)
        return self.data.loc[mask]


def main():
    parser = ParserCBRF()
    parser.start()

    folder_path = Path(__file__).parent / 'parsed_data'
    parser.load_all_data(folder_path)

    data_manager = DataManager(parser.data)

    latest_data = data_manager.get_latest()
    print("Последние данные: Дата =", latest_data['Дата'], "Объем =", latest_data['Объем'])
    print("Среднее значение по колонке 'Объем':", data_manager.get_average('Объем'))

    print("Данные за период с 01.01.2020 по 31.12.2024:")
    data_2020_to_2024 = data_manager.get_data_range('01.01.2020', '31.12.2024')
    if data_2020_to_2024.empty:
        print("Нет данных для указанного периода.")
    else:
        print(data_2020_to_2024.to_string(index=False))

    print("Данные по конкретной дате (например, 05.01.2024):")
    specific_date_data = data_manager.get_by_date('2024-01-05')
    if specific_date_data.empty:
        print("Нет данных для указанной даты.")
    else:
        print(specific_date_data.to_string(index=False))


if __name__ == "__main__":
    main()
