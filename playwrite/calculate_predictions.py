import datetime
from collections import defaultdict
import json

# Load parsed timetable and attendance
with open('extracted_timetable.json', 'r', encoding='utf-8') as f:
    weekly_timetable = json.load(f)

# Days of week map
# "16 November, 2026 Monday" -> "Monday"
day_map = {}
for full_day, hours in weekly_timetable.items():
    for d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        if d in full_day:
            day_map[d] = hours

print("Available timetable days:", list(day_map.keys()))

# Date range: from today (2026-11-19) to end of instruction (2026-12-01)
# Note: Nov 28 is Convocation. Dec 1 is Last Day Of Instruction.
start_date = datetime.date(2026, 11, 19)
end_date = datetime.date(2026, 12, 1)

# List instructional calendar
calendar_days = []
curr = start_date
while curr <= end_date:
    day_name = curr.strftime("%A")
    # Saturday and Sunday are weekends
    # Also check if any special holiday
    is_instructional = True
    note = ""
    if curr == datetime.date(2026, 11, 28):
        is_instructional = False
        note = "Convocation"
    elif day_name in ['Saturday', 'Sunday']:
        is_instructional = False
        note = "Weekend"
    
    calendar_days.append({
        "date": curr.strftime("%Y-%m-%d"),
        "day": day_name,
        "instructional": is_instructional,
        "note": note
    })
    curr += datetime.timedelta(days=1)

print("\nCalendar from Nov 19 to Dec 1:")
for c in calendar_days:
    print(f"{c['date']} ({c['day']}): {'Instructional' if c['instructional'] else 'No Classes (' + c['note'] + ')'}")

# Count remaining classes per course
# Course codes to track
# APT4006, CBC2000, CIT2500, CIT2501, CIT2502, CIT2503, CIT3402, CSS2264, CSS2265, CSS2285, CSS2286
remaining_classes = defaultdict(int)
schedule_by_date = {}

for c in calendar_days:
    d_str = c['date']
    d_name = c['day']
    if not c['instructional']:
        continue
    
    hours = day_map.get(d_name, [])
    # For today Nov 19, should we include all hours or from hour 4 onwards? Let's check both or count whole day
    # Let's count full remaining classes
    schedule_by_date[d_str] = []
    for h in hours:
        detail = h['details']
        if detail != "Free":
            schedule_by_date[d_str].append(h)
            for code in ['APT4006', 'CBC2000', 'CIT2500', 'CIT2501', 'CIT2502', 'CIT2503', 'CIT3402', 'CSS2264', 'CSS2265', 'CSS2285', 'CSS2286']:
                if code in detail:
                    remaining_classes[code] += 1
                    break

print("\nRemaining class count per course from Nov 19 to Dec 1 (9 instructional days):")
for code, cnt in sorted(remaining_classes.items()):
    print(f"{code}: {cnt} classes left")
