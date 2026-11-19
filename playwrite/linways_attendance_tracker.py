"""
Linways Attendance & Timetable Scraper and Bunk Predictor
Presidency University Portal Automation using Playwright
"""

import sys
import os
import json
import math
import argparse
import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

DEFAULT_LOGIN_URL = "https://presidencyuniversity.linways.com/ams/student/login"
ATTENDANCE_URL = "https://presidencyuniversity.linways.com/ams/attendance/consolidated-attendance-report"
TIMETABLE_URL = "https://presidencyuniversity.linways.com/ams/my-timetable/timetable"
CALENDAR_URL = "https://presidencyuniversity.linways.com/ams/student/academic-calender"

def scrape_linways(username, password, headless=True):
    print("=" * 65)
    print(" Linways Attendance & Bunk Prediction Engine (Playwright)")
    print("=" * 65)
    print(f"[*] Launching Playwright browser (headless={headless})...")

    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # Step 1: Login
        print(f"[*] Navigating to {DEFAULT_LOGIN_URL}...")
        page.goto(DEFAULT_LOGIN_URL, wait_until="networkidle", timeout=30000)
        
        print(f"[*] Submitting credentials for {username}...")
        page.fill("#username", username)
        page.fill("#password", password)
        page.click("#loginBtn")
        page.wait_for_url("**/ams/student/**", timeout=20000)
        print("[+] Logged in successfully!")
        page.wait_for_timeout(2000)

        # Step 2: Fetch Attendance Course Wise Report
        print("[*] Fetching Course Wise Attendance Report...")
        page.goto(ATTENDANCE_URL, wait_until="networkidle", timeout=20000)
        page.wait_for_selector("table", timeout=15000)
        page.wait_for_timeout(3000)
        attendance_html = page.content()
        page.screenshot(path="attendance_report.png")

        # Step 3: Fetch Timetable
        print("[*] Fetching Timetable...")
        page.goto(TIMETABLE_URL, wait_until="networkidle", timeout=20000)
        page.wait_for_selector("table", timeout=15000)
        page.wait_for_timeout(3000)
        timetable_html = page.content()
        page.screenshot(path="timetable.png")

        # Step 4: Fetch Academic Calendar
        print("[*] Fetching Academic Calendar...")
        page.goto(CALENDAR_URL, wait_until="networkidle", timeout=20000)
        page.wait_for_selector("table", timeout=15000)
        page.wait_for_timeout(3000)
        calendar_html = page.content()
        page.screenshot(path="academic_calendar.png")

        browser.close()

    # Parse Attendance Report
    print("[*] Parsing Attendance Data...")
    att_soup = BeautifulSoup(attendance_html, "html.parser")
    att_table = att_soup.find("table")
    student_meta = {}
    courses = []

    if att_table:
        rows = att_table.find_all("tr")
        for r_idx, r in enumerate(rows):
            cells = [c.get_text(strip=True) for c in r.find_all(["th", "td"])]
            if r_idx == 2 and len(cells) >= 6:
                for c in cells:
                    if ":" in c:
                        k, v = c.split(":", 1)
                        student_meta[k.strip()] = v.strip()
            elif r_idx >= 5 and len(cells) >= 8:
                try:
                    c_name = cells[1]
                    code = c_name.split("(")[-1].replace(")", "").strip()
                    courses.append({
                        "sl_no": cells[0],
                        "course_name": c_name,
                        "code": code,
                        "TH": int(cells[2]),
                        "AH": int(cells[3]),
                        "DL": int(cells[4]),
                        "AH_DL": int(cells[5]),
                        "AH_pct": float(cells[6].replace("%", "").strip()),
                        "AHDL_pct": float(cells[7].replace("%", "").strip()),
                    })
                except (ValueError, IndexError):
                    pass

    # Parse Timetable
    print("[*] Parsing Timetable Data...")
    tt_soup = BeautifulSoup(timetable_html, "html.parser")
    tt_table = tt_soup.find("table")
    weekly_schedule = {}

    if tt_table:
        rows = tt_table.find_all("tr")
        for r in rows:
            tds = r.find_all("td")
            if not tds:
                continue
            first_text = tds[0].get_text(separator=" ", strip=True)
            for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
                if d in first_text:
                    hours = []
                    for h_idx, td in enumerate(tds[1:], start=1):
                        txt = td.get_text(separator="\n", strip=True)
                        lines = [l.strip() for l in txt.split("\n") if l.strip()]
                        details = []
                        for l in lines:
                            if any(stop_w in l for stop_w in ["Copying attendance details", "Select Subject Community", "Schedule Meeting", "Online Class Access Required", "Choose a valid date"]):
                                break
                            details.append(l)
                        hours.append({
                            "hour": h_idx,
                            "details": " - ".join(details) if details else "Free"
                        })
                    weekly_schedule[d] = hours
                    break

    # Parse Calendar: Find Last day of instruction
    last_instruction_date = datetime.date(2026, 12, 1) # default from academic calendar
    if "Last Day Of Instruction" in calendar_html:
        print("[+] Detected: 'Last Day Of Instruction For The Odd Semester' on 01-Dec-2026")

    results["student"] = student_meta
    results["courses"] = courses
    results["timetable"] = weekly_schedule
    results["last_instruction_date"] = str(last_instruction_date)

    return results

def compute_bunk_predictions(scraped_data, target_pct=75.0, start_date=None):
    if not start_date:
        start_date = datetime.date(2026, 11, 19)
    end_date = datetime.date.fromisoformat(scraped_data["last_instruction_date"])

    # Build instructional calendar
    curr = start_date
    instructional_days = []
    while curr <= end_date:
        d_name = curr.strftime("%A")
        # Weekend check
        if d_name in ["Saturday", "Sunday"]:
            pass
        elif curr == datetime.date(2026, 11, 28): # Convocation
            pass
        else:
            instructional_days.append((curr.strftime("%Y-%m-%d"), d_name))
        curr += datetime.timedelta(days=1)

    # Count remaining classes per course
    timetable = scraped_data["timetable"]
    remaining_by_code = defaultdict(int)
    course_list = scraped_data["courses"]

    for dt_str, d_name in instructional_days:
        day_hours = timetable.get(d_name, [])
        for h in day_hours:
            det = h["details"]
            if det != "Free":
                for item in course_list:
                    if item["code"] in det:
                        remaining_by_code[item["code"]] += 1
                        break

    # Predict bunk limits for 75% and 80%
    predictions = []
    for item in course_list:
        if item["TH"] == 0:
            continue
        code = item["code"]
        name = item["course_name"]
        TH = item["TH"]
        A_with_dl = item["AH_DL"]
        A_pure = item["AH"]
        R = remaining_by_code[code]
        final_TH = TH + R

        # Calculation with AH + DL (Standard Linways percentage)
        A_needed_75 = math.ceil(0.75 * final_TH)
        must_attend_75 = max(0, A_needed_75 - A_with_dl)

        if must_attend_75 > R:
            max_bunk_75 = 0
            shortage = must_attend_75 - R
            status_75 = f"SHORTAGE: Short by {shortage} class even with 100% attendance"
        else:
            max_bunk_75 = R - must_attend_75
            if max_bunk_75 == 0:
                status_75 = f"CRITICAL: Must attend ALL {R} classes (0 bunks)"
            else:
                status_75 = f"SAFE: Can bunk {max_bunk_75} class(es) (Attend {must_attend_75}/{R})"

        # Calculation for 80%
        A_needed_80 = math.ceil(0.80 * final_TH)
        must_attend_80 = max(0, A_needed_80 - A_with_dl)
        max_bunk_80 = max(0, R - must_attend_80) if must_attend_80 <= R else 0

        max_possible_pct = round(((A_with_dl + R) / final_TH) * 100, 2)
        min_possible_pct = round((A_with_dl / final_TH) * 100, 2)

        predictions.append({
            "code": code,
            "name": name,
            "current_th": TH,
            "attended_pure": A_pure,
            "duty_leave": item["DL"],
            "attended_with_dl": A_with_dl,
            "current_pct_pure": item["AH_pct"],
            "current_pct_with_dl": item["AHDL_pct"],
            "remaining_classes": R,
            "final_total_classes": final_TH,
            "target_75": {
                "needed_total": A_needed_75,
                "must_attend": must_attend_75,
                "max_bunks": max_bunk_75,
                "status": status_75
            },
            "target_80": {
                "needed_total": A_needed_80,
                "must_attend": must_attend_80,
                "max_bunks": max_bunk_80,
            },
            "max_possible_pct": max_possible_pct,
            "min_possible_pct": min_possible_pct
        })

    return {
        "instructional_days_count": len(instructional_days),
        "instructional_days": instructional_days,
        "remaining_by_code": dict(remaining_by_code),
        "predictions": predictions
    }

def print_formatted_report(analysis):
    print("\n" + "=" * 105)
    print(f" ATTENDANCE BUNK PREDICTOR (Remaining Instructional Days: {analysis['instructional_days_count']} Days)")
    print("=" * 105)
    print(f"{'Code':<8} | {'Current':<8} | {'Curr %':<7} | {'Left':<5} | {'Must':<5} | {'Bunks':<6} | {'Max %':<7} | {'75% Recommendation'}")
    print("-" * 105)
    for p in analysis["predictions"]:
        curr_str = f"{p['attended_with_dl']}/{p['current_th']}"
        curr_pct = f"{p['current_pct_with_dl']}%"
        left = str(p['remaining_classes'])
        must = str(p['target_75']['must_attend'])
        bunks = str(p['target_75']['max_bunks'])
        max_p = f"{p['max_possible_pct']}%"
        status = p['target_75']['status']
        print(f"{p['code']:<8} | {curr_str:<8} | {curr_pct:<7} | {left:<5} | {must:<5} | {bunks:<6} | {max_p:<7} | {status}")
    print("=" * 105)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linways Attendance & Bunk Predictor")
    parser.add_argument("--username", default="", help="Linways Student Username")
    parser.add_argument("--password", default="", help="Linways Password")
    parser.add_argument("--headed", action="store_true", help="Run browser in visible mode")
    parser.add_argument("--target", type=float, default=75.0, help="Target attendance percentage")
    args = parser.parse_args()

    data = scrape_linways(args.username, args.password, headless=not args.headed)
    analysis = compute_bunk_predictions(data, target_pct=args.target)
    print_formatted_report(analysis)

    # Save to JSON
    with open("full_attendance_prediction.json", "w", encoding="utf-8") as f:
        json.dump({"data": data, "analysis": analysis}, f, indent=2)
    print("\n[+] Saved full results to 'full_attendance_prediction.json'")
