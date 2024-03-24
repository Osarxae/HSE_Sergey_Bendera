with open('traders.txt', 'r') as file:
    inn_list = [line.strip() for line in file if line.strip()]
    import json

    with open('traders.json', 'r') as file:
        traders_data = json.load(file)

    traders_info = {}
    for inn in inn_list:
        for trader in traders_data:
            if trader['inn'] == inn:
                traders_info[inn] = {'ogrn': trader['ogrn'], 'address': trader['address']}
                break
import csv

with open('traders.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['inn', 'ogrn', 'address'])
    for inn, info in traders_info.items():
        writer.writerow([inn, info['ogrn'], info['address']])

import re
def find_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    return re.findall(email_pattern, text)
def find_all_emails(dataset):
    email_dict = {}
    for message in dataset:
        emails = find_emails(message['msg_text'])
        if emails:
            publisher_inn = message['publisher_inn']
            if publisher_inn not in email_dict:
                email_dict[publisher_inn] = set()
            email_dict[publisher_inn].update(emails)
    return email_dict

def save_emails_to_file(email_dict, filename):
    with open(filename, 'w') as file:
        json.dump(email_dict, file, ensure_ascii=False, indent=4)

with open('dataset.json', 'r') as file:
    dataset = json.load(file)

email_dict = find_all_emails(dataset)
save_emails_to_file(email_dict, 'emails.json')