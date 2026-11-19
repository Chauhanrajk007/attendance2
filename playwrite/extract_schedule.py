from bs4 import BeautifulSoup
import json

with open('timetable_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

table = soup.find('table')
all_tr = table.find_all('tr')
print(f"Total tr found: {len(all_tr)}")

day_blocks = []
current_day = None

for tr in all_tr:
    tds = tr.find_all('td')
    if not tds:
        continue
    first_td_text = tds[0].get_text(separator=' ', strip=True)
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
        if day in first_td_text:
            day_blocks.append((day, first_td_text, tds))
            break

print(f"Found {len(day_blocks)} day rows")
results = {}
for day, label, tds in day_blocks:
    hours = []
    # tds[1:] has hour 1 to 8
    for h_num, td in enumerate(tds[1:], start=1):
        # Find all direct text or main div
        text_content = td.get_text(separator='\n', strip=True)
        lines = [l.strip() for l in text_content.split('\n') if l.strip()]
        class_details = []
        for l in lines:
            if any(term in l for term in ['Copying attendance details', 'Select Subject Community', 'Schedule Meeting', 'Online Class Access Required', 'Choose a valid date']):
                break
            class_details.append(l)
        hours.append({
            "hour": h_num,
            "details": " - ".join(class_details) if class_details else "Free"
        })
    results[label] = hours

print(json.dumps(results, indent=2))
with open('extracted_timetable.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
