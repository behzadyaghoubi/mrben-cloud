import requests
from bs4 import BeautifulSoup
import csv
import re

URL = 'https://www.lotteryextreme.com/canada/lottomax-results'
CSV_FILE = 'lotto_max_history.csv'

def fetch_lotto_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for cx in soup.select('td.cx'):
        m = re.search(r'\((\d{4}-\d{2}-\d{2})', cx.text)
        if not m:
            continue
        date = m.group(1)
        # پیدا کردن ul.displayball بعدی در ساختار جدول
        tr = cx.find_parent('tr')
        next_tr = tr.find_next_sibling('tr')
        if not next_tr:
            continue
        ul = next_tr.find('ul', class_='displayball')
        if not ul:
            continue
        nums = [li.text.strip() for li in ul.find_all('li') if li.text.strip().isdigit()]
        if len(nums) >= 7:
            results.append([date] + nums[:7])
    return results

def save_to_csv(data):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7'])
        writer.writerows(data)

def main():
    data = fetch_lotto_data()
    save_to_csv(data)
    print(f"Saved {len(data)} draws to {CSV_FILE}")

if __name__ == '__main__':
    main()