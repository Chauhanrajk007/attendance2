from bs4 import BeautifulSoup
import json

with open('academic_calendar_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Let's inspect calendar items
events = []
cells = soup.find_all(['td', 'div', 'p'])
for c in cells:
    txt = c.get_text(separator=' ', strip=True)
    if any(m in txt for m in ['November', 'December', 'Convocation', 'Instruction', 'Holiday', 'Deepavali', 'Rajyotsava']):
        if len(txt) < 200:
            events.append(txt)

print("Unique event mentions:")
seen = set()
for e in events:
    if e not in seen:
        seen.add(e)
        print("-", e)
