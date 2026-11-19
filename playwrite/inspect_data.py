import json
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def inspect_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Logging in...")
        page.goto('https://presidencyuniversity.linways.com/ams/student/login', wait_until='networkidle')
        page.fill('#username', '2024/448')
        page.fill('#password', 'Komala@9821')
        page.click('#loginBtn')
        page.wait_for_url('**/ams/student/**', timeout=15000)
        time.sleep(2)

        # 1. Attendance Course Wise Report
        print("\n--- 1. Visiting Attendance Course Wise Report ---")
        page.goto('https://presidencyuniversity.linways.com/ams/attendance/consolidated-attendance-report', wait_until='networkidle')
        time.sleep(3)
        page.screenshot(path='attendance_report.png', full_page=True)
        with open('attendance_page.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Attendance page title:", page.title())
        # Print table contents if any
        tables = page.locator('table').all()
        print(f"Found {len(tables)} tables on attendance page")
        for idx, tbl in enumerate(tables):
            print(f"Table {idx}:")
            print(tbl.inner_text()[:1000])

        # 2. Timetable
        print("\n--- 2. Visiting Timetable ---")
        page.goto('https://presidencyuniversity.linways.com/ams/my-timetable/timetable', wait_until='networkidle')
        time.sleep(3)
        page.screenshot(path='timetable.png', full_page=True)
        with open('timetable_page.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Timetable page title:", page.title())
        tables = page.locator('table').all()
        print(f"Found {len(tables)} tables on timetable page")
        for idx, tbl in enumerate(tables):
            print(f"Table {idx}:")
            print(tbl.inner_text()[:1500])

        # 3. Academic Calendar
        print("\n--- 3. Visiting Academic Calendar ---")
        page.goto('https://presidencyuniversity.linways.com/ams/student/academic-calender', wait_until='networkidle')
        time.sleep(3)
        page.screenshot(path='academic_calendar.png', full_page=True)
        with open('academic_calendar_page.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Calendar page title:", page.title())
        tables = page.locator('table').all()
        print(f"Found {len(tables)} tables on calendar page")
        for idx, tbl in enumerate(tables):
            print(f"Table {idx}:")
            print(tbl.inner_text()[:1000])

        browser.close()

if __name__ == '__main__':
    inspect_pages()
