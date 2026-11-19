# AttendTrack — Campus Attendance & Bunk Predictor

A clean, modern, and simple attendance dashboard and schedule predictor. Built with Flask, lightweight vanilla JavaScript, and Grok AI.

---

## 🚀 Quick Start

1. **Start the web application**:
   ```bash
   python app.py
   ```
2. **Open in your browser**:
   ```
   http://127.0.0.1:5000
   ```

---

## 🌟 Key Features

### 1. Simple, Clean & Modern UI (No Purple Gradients)
- Crisp slate, white, and soft neutral color scheme.
- Clear status badges:
  - 🟢 **Safe ($\ge 75\%$)**: Soft emerald
  - 🟡 **Warning ($65\% - 74.9\%$)**: Warm amber
  - 🔴 **Critical ($< 65\%$)**: Soft rose red
- Completely free of purple gradients or cluttered styling.

### 2. Flexible Data Ingestion (No Playwright Required on Website)
- **1-Click Campus Data**: Instant preview with your pre-extracted Linways dataset (Chauhan Raj K, 13 courses, odd semester).
- **Manual Upload**: Upload attendance reports (`.html`, `.csv`, `.json`), timetables (`.html`, `.json`), or academic calendars.
- **Friend API Sync (`POST /api/import-data`)**: Your friend can run Playwright separately and directly send JSON to the dashboard.

### 3. Interactive Bunk Simulator & Day-Off Planner
- **Course-by-Course Stepper**: Adjust bunks (`+` / `-`) or attended classes for each subject and see the projected percentage and difference in real-time.
- **Safe Bunk Calculator**: Calculates the maximum number of classes you can skip while remaining above 75% (or your chosen target of 80% / 85%).
- **Recovery Calculator**: If attendance is below 75%, tells you exactly how many consecutive classes you must attend to recover.
- **Quick Day-Off Planner**: Click **Mon**, **Tue**, **Wed**, **Thu**, **Fri**, or **Sat** to immediately simulate missing all classes on that day.
- **Global Bunk Slider**: Test what happens if you take $N$ total classes off.

### 4. Schedule Projections till Last Working Day
- Connects your weekly lecture/lab timetable with the semester's **Last Working Day** (e.g. Dec 01, 2026).
- Accurately counts how many classes of each subject remain before classes end.
- Displays **Best-Case %** (if you attend every remaining class) vs. **Worst-Case %** (if you bunk all of them).

### 5. Grok AI Attendance Advisor
- Integrates with the **xAI Grok API** using your key.
- Analyzes your attendance and timetable to provide high-impact strategy recommendations:
  - Highlights critical subjects you must never bunk.
  - Suggests low-risk subjects where skipping is safe.
  - Answers custom student queries (e.g., *"Can I skip Blockchain class tomorrow?"*).
- Includes a smart local heuristic engine fallback.

---

## 🤝 For Your Friend (Playwright Integration API)

Your friend can keep their Playwright script completely independent and push scraped data using a simple HTTP POST request:

```python
import requests

data = {
    "profile": {
        "Student Name": "CHAUHAN RAJ K",
        "Roll No": "20241CIT0119",
        "Batch/Section": "2024CIT02",
        "Department": "PSAIAC",
        "Term": "S5"
    },
    "courses": [
        {
            "sl_no": "1",
            "course_name": "Logical and Critical Thinking",
            "course_code": "APT4006",
            "th": 20,
            "ah": 14,
            "dl": 2,
            "ah_dl": 16,
            "total_pct": 80.0
        },
        {
            "sl_no": "2",
            "course_name": "Foundations of Blockchain Technology",
            "course_code": "CBC2000",
            "th": 34,
            "ah": 21,
            "dl": 3,
            "ah_dl": 24,
            "total_pct": 70.59
        }
    ],
    "timetable": {
        "Monday": [
            {"period": 1, "course_code": "CBC2000", "course_name": "Foundations of Blockchain Technology", "timing": "08:50 AM - 09:45 AM", "room": "NS04"}
        ]
    },
    "calendar": {
        "last_working_day": "2026-12-01"
    }
}

response = requests.post("http://localhost:5000/api/import-data", json=data)
print(response.json())
```
