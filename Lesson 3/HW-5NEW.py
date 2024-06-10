import json
import csv
import re
import zoneinfo
from collections import defaultdict

# Константа для часового пояса Москвы
TZ_MOSCOW = zoneinfo.ZoneInfo("Europe/Moscow")


def read_inn_set(filename: str) -> set:
    """Чтение ИНН из файла и возврат их в виде множества."""
    with open(filename, "r") as f:
        return set(line.strip() for line in f)


def read_json_data(filename: str) -> list:
    """Чтение данных из JSON файла."""
    with open(filename, "r") as f:
        return json.load(f)


def filter_data_by_inn(data: list, inn_set: set) -> list:
    """Фильтрация данных по ИНН."""
    return [item for item in data if item.get('inn') in inn_set]


def export_to_csv(data: list, filename: str) -> None:
    """Экспорт данных в CSV файл."""
    with open(filename, 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=';')
        csv_writer.writerow(['ИНН', 'ОГРН', 'Адрес'])
        for item in data:
            csv_writer.writerow([item.get('inn'), item.get('ogrn'), item.get('address')])


def find_emails(text: str) -> list:
    """Функция для поиска email-адресов в тексте."""
    email_pattern = re.compile(r'\b[0-9a-zA-Z.-_]+@[0-9a-zA-Z.-_]+\.[a-zA-Z]+\b')
    return email_pattern.findall(text)


def extract_emails(messages: list) -> dict:
    """Извлечение email адресов из сообщений."""
    emails = defaultdict(set)
    for msg in messages:
        found_emails = find_emails(msg.get('msg_text', ''))
        for email in found_emails:
            emails[msg.get('publisher_inn')].add(email.lower())
    return {key: list(value) for key, value in emails.items()}


def execute_pipeline() -> None:
    """Основная функция для выполнения всех шагов обработки данных."""
    inn_set = read_inn_set("traders.txt")
    trader_data = read_json_data("traders.json")
    filtered_data = filter_data_by_inn(trader_data, inn_set)
    export_to_csv(filtered_data, 'traders_output.csv')

    message_data = read_json_data("1000_efrsb_messages.json")
    email_mapping = extract_emails(message_data)
    with open('emails_output.json', "w") as f:
        json.dump(email_mapping, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    execute_pipeline()
