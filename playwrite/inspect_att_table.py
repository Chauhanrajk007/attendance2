from bs4 import BeautifulSoup
import json

with open('attendance_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')
for i, r in enumerate(rows):
    cells = [c.get_text(strip=True) for c in r.find_all(['th', 'td'])]
    print(f"Row {i} (len={len(cells)}): {cells}")
