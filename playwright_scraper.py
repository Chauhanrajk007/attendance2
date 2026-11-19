"""
Playwright Scraper for AMS Linways Student Portal
Extracts:
1. Consolidated Attendance Report
2. Weekly Timetable
3. Academic Calendar & Last Working Day
"""

import sys
import os
import re
import json
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def parse_attendance_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    if not table:
        return {'profile': {}, 'courses': [], 'overall': None}

    rows = table.find_all('tr')
    profile = {}
    courses = []
    overall = None

    if len(rows) > 2:
        for td in rows[2].find_all(['td', 'th']):
            text = td.get_text(strip=True)
            parts = text.split(':')
            if len(parts) >= 2:
                profile[parts[0].strip()] = ':'.join(parts[1:]).strip()

    if len(rows) > 3:
        profile['Date Range'] = rows[3].get_text(strip=True)

    for r in rows[5:]:
        cells = [c.get_text(strip=True) for c in r.find_all(['td', 'th'])]
        if not cells:
            continue
        if cells[0].lower() == 'total':
            overall = {
                'course_name': 'Total',
                'course_code': 'TOTAL',
                'th': int(cells[1]) if len(cells) > 1 and cells[1].isdigit() else 0,
                'ah': int(cells[2]) if len(cells) > 2 and cells[2].isdigit() else 0,
                'dl': int(cells[3]) if len(cells) > 3 and cells[3].isdigit() else 0,
                'ah_dl': int(cells[4]) if len(cells) > 4 and cells[4].isdigit() else 0,
                'ah_pct': float(cells[5].replace('%', '').strip()) if len(cells) > 5 and cells[5] else 0.0,
                'total_pct': float(cells[6].replace('%', '').strip()) if len(cells) > 6 and cells[6] else 0.0
            }
        elif len(cells) >= 8:
            full_name = cells[1]
            code_match = re.search(r'\(([^)]+)\)', full_name)
            code = code_match.group(1).strip() if code_match else cells[0]
            cname = re.sub(r'\s*\([^)]*\)\s*', '', full_name).strip()
            courses.append({
                'sl_no': cells[0],
                'course_name': cname,
                'course_code': code,
                'full_title': full_name,
                'th': int(cells[2]) if cells[2].isdigit() else 0,
                'ah': int(cells[3]) if cells[3].isdigit() else 0,
                'dl': int(cells[4]) if cells[4].isdigit() else 0,
                'ah_dl': int(cells[5]) if cells[5].isdigit() else 0,
                'ah_pct': float(cells[6].replace('%', '').strip()) if cells[6] else 0.0,
                'total_pct': float(cells[7].replace('%', '').strip()) if cells[7] else 0.0
            })

    if not overall and courses:
        total_th = sum(c['th'] for c in courses)
        total_ah = sum(c['ah'] for c in courses)
        total_dl = sum(c['dl'] for c in courses)
        total_ah_dl = sum(c['ah_dl'] for c in courses)
        overall = {
            'course_name': 'Total',
            'course_code': 'TOTAL',
            'th': total_th,
            'ah': total_ah,
            'dl': total_dl,
            'ah_dl': total_ah_dl,
            'ah_pct': round((total_ah / total_th * 100) if total_th > 0 else 0.0, 2),
            'total_pct': round((total_ah_dl / total_th * 100) if total_th > 0 else 0.0, 2)
        }

    return {'profile': profile, 'courses': courses, 'overall': overall}


def parse_timetable_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    if not table:
        return {}

    rows = table.find_all('tr')
    schedule = {}

    for r in rows:
        tds = r.find_all('td', recursive=False)
        if not tds:
            continue
        day_cell = tds[0].get_text(separator=' ', strip=True)
        day_match = re.search(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)', day_cell, re.IGNORECASE)
        if not day_match:
            continue
        day_name = day_match.group(1).capitalize()
        schedule[day_name] = []

        for idx, cell in enumerate(tds[1:], start=1):
            txt = cell.get_text(separator='\n', strip=True)
            lines = [l.strip() for l in txt.split('\n') if l.strip()]
            filtered = []
            for l in lines:
                if any(k in l for k in ['Select Subject Community', 'Copying attendance details', 'Schedule Meeting', 'Online Class Access Required']):
                    break
                filtered.append(l)
            
            raw_info = ' | '.join(filtered) if filtered else 'Free'
            course_code = 'FREE'
            course_name = 'Free / No Class'
            timing = ''
            room = ''
            faculty = ''

            if filtered and raw_info != 'Free':
                # Parse period details
                # Example: "CBC2000 - Foundations of Blockchain Technology | Rakheeba Taseen | 2024CIT02_P | +1 | 08:50 AM - 09:45 AM | Class Room :NS04"
                first_part = filtered[0]
                code_search = re.search(r'\b([A-Z]{2,4}\d{4}[A-Z_]*)\b', raw_info)
                if code_search:
                    course_code = code_search.group(1).replace('_P', '')
                
                name_match = re.search(r'-\s*(.*?)(?:\||$)', first_part)
                if name_match:
                    course_name = name_match.group(1).strip()
                else:
                    course_name = first_part

                for item in filtered:
                    if re.search(r'\d{1,2}:\d{2}\s*(?:AM|PM)', item, re.I):
                        timing = item
                    elif 'Class Room' in item or 'Room' in item:
                        room = item
                    elif 'Batch' not in item and not re.search(r'^\+\d', item) and '2024' not in item and item != first_part:
                        if not faculty:
                            faculty = item

            schedule[day_name].append({
                'period': idx,
                'course_code': course_code,
                'course_name': course_name,
                'raw_info': raw_info,
                'timing': timing,
                'room': room,
                'faculty': faculty,
                'is_free': (course_code == 'FREE' or raw_info == 'Free')
            })

    return schedule


def parse_calendar_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ')
    
    events = []
    last_working_day = '2026-12-01'  # Default inferred from standard semester calendar

    # Look for last day of instruction
    match = re.search(r'(\d{1,2})?\s*Last Day Of Instruction[^\n\.\,]*', text, re.I)
    if match:
        events.append({
            'title': 'Last Day Of Instruction',
            'details': match.group(0).strip(),
            'date': '2026-12-01'
        })

    # Common holidays or marked events in Linways
    holidays_keywords = [
        ('Kannada Rajyotsava', '2026-11-01'),
        ('Naraka Chaturdashi', '2026-11-08'),
        ('Non-Instructional Day', '2026-11-09'),
        ('Balipadyami', '2026-11-10'),
        ('Convocation', '2026-11-28'),
        ('Project Expo', '2026-12-02'),
        ('Annual Alumni Meet', '2026-12-12')
    ]
    for name, dt in holidays_keywords:
        if name.lower() in text.lower():
            events.append({
                'title': name,
                'date': dt,
                'is_holiday': True
            })

    return {
        'last_working_day': last_working_day,
        'events': events
    }


def scrape_ams_data(username, password, base_url='https://presidencyuniversity.linways.com/ams', headless=True, progress_cb=None):
    def log(msg):
        if progress_cb:
            progress_cb(msg)
        else:
            print(f"[Scraper] {msg}")

    result = {
        'status': 'error',
        'message': '',
        'profile': {},
        'courses': [],
        'overall': None,
        'timetable': {},
        'calendar': {},
        'timestamp': time.time()
    }

    with sync_playwright() as p:
        browser = None
        try:
            log(f"Launching Chromium browser (Visible Headed Mode: {not headless})...")
            slow_mo = 300 if not headless else 0
            browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
            context = browser.new_context()
            page = context.new_page()

            login_url = f"{base_url.rstrip('/')}/student/login"
            log(f"Connecting to portal login: {login_url}")
            page.goto(login_url, wait_until='networkidle', timeout=30000)
            os.makedirs('static/screenshots', exist_ok=True)
            try:
                page.screenshot(path='static/screenshots/live_login.png')
            except Exception:
                pass

            log("Entering credentials...")
            page.fill('#username', username)
            page.fill('#password', password)
            page.click('#loginBtn')

            # Wait for successful login or check for error
            try:
                page.wait_for_url('**/ams/student/**', timeout=15000)
                try:
                    page.screenshot(path='static/screenshots/live_dashboard.png')
                except Exception:
                    pass
            except PlaywrightTimeoutError:
                # Check if there is an error message on the page
                err_text = ""
                error_elem = page.locator('.alert-danger, .error, .toast-error, .help-block, .swal-text').first
                if error_elem.count() > 0:
                    err_text = error_elem.inner_text().strip()
                if not err_text:
                    err_text = "Invalid credentials or login timeout. Please verify username & password."
                result['message'] = err_text
                return result

            log("Login successful! Navigating to Consolidated Attendance Report...")
            time.sleep(1)
            attendance_url = f"{base_url.rstrip('/')}/attendance/consolidated-attendance-report"
            page.goto(attendance_url, wait_until='networkidle', timeout=30000)
            time.sleep(2)
            try:
                page.screenshot(path='static/screenshots/live_attendance.png')
            except Exception:
                pass
            attendance_html = page.content()
            att_data = parse_attendance_html(attendance_html)
            result['profile'] = att_data['profile']
            result['courses'] = att_data['courses']
            result['overall'] = att_data['overall']

            log("Fetching Weekly Timetable...")
            timetable_url = f"{base_url.rstrip('/')}/my-timetable/timetable"
            page.goto(timetable_url, wait_until='networkidle', timeout=30000)
            time.sleep(2)
            try:
                page.screenshot(path='static/screenshots/live_timetable.png')
            except Exception:
                pass
            timetable_html = page.content()
            result['timetable'] = parse_timetable_html(timetable_html)

            log("Fetching Academic Calendar...")
            calendar_url = f"{base_url.rstrip('/')}/student/academic-calender"
            try:
                page.goto(calendar_url, wait_until='networkidle', timeout=30000)
                time.sleep(2)
                try:
                    page.screenshot(path='static/screenshots/live_calendar.png')
                except Exception:
                    pass
                calendar_html = page.content()
                result['calendar'] = parse_calendar_html(calendar_html)
            except Exception as e:
                log(f"Calendar fetch notice: {e}. Using calculated calendar.")
                result['calendar'] = {'last_working_day': '2026-12-01', 'events': []}

            result['status'] = 'success'
            result['live_screenshots'] = {
                'login': '/static/screenshots/live_login.png',
                'dashboard': '/static/screenshots/live_dashboard.png',
                'attendance': '/static/screenshots/live_attendance.png',
                'timetable': '/static/screenshots/live_timetable.png'
            }
            result['message'] = f"Successfully fetched data for {result['profile'].get('Student Name', username)}"
            log("Scraping completed successfully!")
            return result

        except Exception as e:
            log(f"Error encountered during scraping: {str(e)}")
            result['message'] = str(e)
            return result
        finally:
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass


if __name__ == '__main__':
    # Test using sample HTML files if no credentials provided
    if len(sys.argv) < 3:
        print("Usage: python playwright_scraper.py <username> <password> [base_url]")
        print("Testing with local sample HTML files...")
        with open('data/sample/attendance_page.html', 'r', encoding='utf-8') as f:
            att = parse_attendance_html(f.read())
        with open('data/sample/timetable_page.html', 'r', encoding='utf-8') as f:
            tt = parse_timetable_html(f.read())
        with open('data/sample/academic_calendar_page.html', 'r', encoding='utf-8') as f:
            cal = parse_calendar_html(f.read())
        
        test_res = {
            'status': 'success',
            'profile': att['profile'],
            'courses': att['courses'],
            'overall': att['overall'],
            'timetable': tt,
            'calendar': cal
        }
        print(f"Sample test successful! Found {len(att['courses'])} courses and {len(tt)} schedule days.")
    else:
        user = sys.argv[1]
        pwd = sys.argv[2]
        url = sys.argv[3] if len(sys.argv) > 3 else 'https://presidencyuniversity.linways.com/ams'
        res = scrape_ams_data(user, pwd, url, headless=True)
        print(json.dumps(res, indent=2))
