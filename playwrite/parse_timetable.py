from bs4 import BeautifulSoup
import json

with open('timetable_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Let's inspect the main timetable table (table 0)
table = soup.find('table')
if table:
    rows = table.find_all('tr')
    print(f"Number of rows: {len(rows)}")
    for r_idx, r in enumerate(rows):
        cells = r.find_all(['th', 'td'])
        cell_texts = [c.get_text(separator=' ', strip=True) for c in cells]
        print(f"Row {r_idx}: {cell_texts}")
