import requests
from bs4 import BeautifulSoup
import csv
import re
import time
from datetime import datetime, timedelta

CSV_FILE = 'lotto_max_history_extended.csv'

def fetch_month_data(year, month):
    """جمع‌آوری داده‌های یک ماه خاص"""
    url = 'https://www.lotteryextreme.com/canada/lottomax-results'
    data = {
        'ig': 'lottomax-results',
        'mode': 'month',
        'year_month': f'{year}-{month:02d}'
    }
    
    try:
        response = requests.post(url, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for cx in soup.find_all('td', class_='cx'):
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
                if 'dbx' in li.get('class', []):
                    break
                match = re.search(r'\d+', li.text)
                if match:
                    nums.append(match.group())
            
            if len(nums) == 7:
                results.append([date] + nums)
        
        print(f"Fetched {len(results)} draws for {year}-{month:02d}")
        return results
    
    except Exception as e:
        print(f"Error fetching {year}-{month:02d}: {e}")
        return []

def fetch_extended_data():
    """جمع‌آوری داده‌های چندین سال اخیر"""
    all_results = []
    
    # شروع از سال 2020 تا 2025
    for year in range(2020, 2026):
        for month in range(1, 13):
            # اگر ماه آینده است، متوقف شو
            if year == 2025 and month > 7:
                break
            if year == 2020 and month < 9:  # لوتومکس از سپتامبر 2009 شروع شد
                continue
                
            results = fetch_month_data(year, month)
            all_results.extend(results)
            
            # کمی صبر کنیم تا سرور را تحت فشار نگذاریم
            time.sleep(1)
    
    return all_results

def save_to_csv(data):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7'])
        writer.writerows(data)

def main():
    print("Starting extended data collection...")
    data = fetch_extended_data()
    save_to_csv(data)
    print(f"Saved {len(data)} total draws to {CSV_FILE}")

if __name__ == '__main__':
    main()