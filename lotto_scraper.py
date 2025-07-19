import requests
from bs4 import BeautifulSoup
import csv
import re

# URL = 'https://www.lotteryextreme.com/canada/lottomax-results'
HTML_FILE = 'lottomax_results.html'
CSV_FILE = 'lotto_max_history.csv'

def fetch_lotto_data():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    cxs = soup.find_all('td', class_='cx')
    print(f"Found {len(cxs)} td.cx tags")
    for i, cx in enumerate(cxs):
        m = re.search(r'\((\d{4}-\d{2}-\d{2})', cx.text)
        if not m:
            continue
        date = m.group(1)
        tr = cx.find_parent('tr')
        next_tr = tr.find_next_sibling('tr')
        if not next_tr:
            continue
        ul = next_tr.find('ul', class_='displayball')
        if not ul:
            continue
        nums = []
        for li in ul.find_all('li'):
            print(f"li: '{li}' text: '{li.text}' class: {li.get('class', [])}")
            if 'dbx' in li.get('class', []):
                break
            match = re.search(r'\d+', li.text)
            if match:
                nums.append(match.group())
        print(f"{date}: {nums}")
        if len(nums) == 7:
            results.append([date] + nums)
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