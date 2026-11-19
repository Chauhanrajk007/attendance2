from bs4 import BeautifulSoup
import json

with open('attendance_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')

data = []
headers = []
for idx, r in enumerate(rows):
    if idx == 0: # Title "COURSE WISE REPORT"
        continue
    if idx == 1: # Date range
        continue
    cells = r.find_all(['th', 'td'])
    cell_texts = [c.get_text(strip=True) for c in cells]
    if not headers:
        headers = cell_texts
    else:
        if len(cell_texts) >= len(headers):
            row_dict = dict(zip(headers, cell_texts))
            data.append(row_dict)

print("Headers:", headers)
print("Data rows:", len(data))
print(json.dumps(data, indent=2))

with open('attendance_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
