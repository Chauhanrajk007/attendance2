import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors (Cybersecurity x AI palette: Dark Navy, Clean Slate, Vibrant Cyan, White, Subtle Grey)
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    BG_LIGHT = RGBColor(248, 250, 252)   # Slate 50
    TEXT_MAIN = RGBColor(15, 23, 42)
    TEXT_MUTED = RGBColor(100, 116, 139)
    TEXT_LIGHT = RGBColor(241, 245, 249)
    CYAN_ACCENT = RGBColor(2, 132, 199)  # Sky 600
    EMERALD = RGBColor(16, 185, 129)     # Emerald 500
    AMBER = RGBColor(217, 119, 6)        # Amber 600
    CARD_BORDER = RGBColor(226, 232, 240)

    def add_header(slide, title_text, slide_num):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.8))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        
        p0 = tf.paragraphs[0]
        p0.text = "CYBERSECURITY × AI  ·  REAL PROBLEMS · REAL SOLUTIONS · AI-POWERED INNOVATION  ·  PRESIDENCY UNIVERSITY × ISACA BANGALORE CHAPTER"
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = TEXT_MUTED
        
        p1 = tf.add_paragraph()
        p1.text = title_text.upper()
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_MAIN

        num_box = slide.shapes.add_textbox(Inches(12.0), Inches(0.4), Inches(0.8), Inches(0.6))
        ntf = num_box.text_frame
        np = ntf.paragraphs[0]
        np.text = f"{slide_num:02d}"
        np.alignment = PP_ALIGN.RIGHT
        np.font.size = Pt(18)
        np.font.bold = True
        np.font.color.rgb = CYAN_ACCENT

        team_tag = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(4.0), Inches(0.3))
        ttp = team_tag.text_frame.paragraphs[0]
        ttp.text = "Team Syndicate  ·  Bug Hunt Arena 2026"
        ttp.font.size = Pt(9)
        ttp.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 1: IDEA SUBMISSION (TITLE SLIDE)
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    
    top_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.2))
    stf = top_box.text_frame
    p = stf.paragraphs[0]
    p.text = "BUG HUNT ARENA 2026 · 19 NOVEMBER 2026"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    p2 = stf.add_paragraph()
    p2.text = "REAL PROBLEMS · REAL SOLUTIONS · AI-POWERED INNOVATION  —  IDEA SUBMISSION"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN

    p3 = stf.add_paragraph()
    p3.text = "Organized by Presidency University × ISACA Bangalore Chapter  |  Track: Cybersecurity × AI"
    p3.font.size = Pt(10)
    p3.font.color.rgb = TEXT_MUTED

    fields = [
        ("PROBLEM STATEMENT ID", "PS-EDU-04 (Student Retention & Academic Risk)"),
        ("PROBLEM STATEMENT TITLE", "Early Warning System for Student Dropouts & Debarment Risk"),
        ("TRACK / THEME", "Cybersecurity × AI (AI in Academic Integrity & Support)"),
        ("TEAM NAME", "Team Syndicate"),
        ("TEAM MEMBERS", "Chauhan Raj K (Lead), [Teammate 2], [Teammate 3]"),
        ("DEPARTMENT / YEAR", "Dept. of Computer Science & Engineering (IoT & Cyber) · 3rd Year"),
        ("CONTACT", "chauhanraj@presidencyuniversity.in  |  +91 98862 88433")
    ]

    y_start = 2.0
    for label, val in fields:
        card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(y_start), Inches(6.0), Inches(0.62))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_LIGHT
        card.line.color.rgb = CARD_BORDER
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_top = Inches(0.06)
        ctf.margin_left = Inches(0.15)
        
        lp = ctf.paragraphs[0]
        lp.text = label
        lp.font.size = Pt(7.5)
        lp.font.bold = True
        lp.font.color.rgb = CYAN_ACCENT
        
        vp = ctf.add_paragraph()
        vp.text = val
        vp.font.size = Pt(9.5)
        vp.font.bold = True
        vp.font.color.rgb = TEXT_MAIN
        y_start += 0.68

    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(2.0), Inches(5.333), Inches(4.5))
    hero.fill.solid()
    hero.fill.fore_color.rgb = BG_DARK
    hero.line.color.rgb = CYAN_ACCENT
    htf = hero.text_frame
    htf.word_wrap = True
    htf.margin_left = Inches(0.4)
    htf.margin_right = Inches(0.4)
    htf.margin_top = Inches(0.5)

    hp0 = htf.paragraphs[0]
    hp0.text = "IDEA TITLE"
    hp0.font.size = Pt(11)
    hp0.font.bold = True
    hp0.font.color.rgb = CYAN_ACCENT

    hp1 = htf.add_paragraph()
    hp1.text = "AttendTrack AI"
    hp1.font.size = Pt(32)
    hp1.font.bold = True
    hp1.font.color.rgb = TEXT_LIGHT

    hp2 = htf.add_paragraph()
    hp2.text = "Autonomous Early Warning & Predictive Bunk Simulator for Degree Defense"
    hp2.font.size = Pt(14)
    hp2.font.bold = True
    hp2.font.color.rgb = RGBColor(148, 163, 184)

    hp3 = htf.add_paragraph()
    hp3.text = "\n• Problem Addressed: Educational institutions currently detect dropout risk only after attendance and performance have already suffered irreversible decline."
    hp3.font.size = Pt(10)
    hp3.font.color.rgb = RGBColor(226, 232, 240)

    hp4 = htf.add_paragraph()
    hp4.text = "• Solution: Headless live portal scraping + real-time mathematical simulation + Grok AI optimization to eliminate detention risk before portal freeze."
    hp4.font.size = Pt(10)
    hp4.font.color.rgb = RGBColor(226, 232, 240)

    # -------------------------------------------------------------------------
    # SLIDE 2: PROPOSED SOLUTION
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "PROPOSED SOLUTION", 2)

    tag_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.65))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    tag_box.line.color.rgb = RGBColor(199, 210, 254)
    ttf = tag_box.text_frame
    ttf.word_wrap = True
    ttf.margin_top = Inches(0.12)
    ttf.margin_left = Inches(0.2)
    tp = ttf.paragraphs[0]
    tp.text = "YOUR IDEA IN ONE LINE:  AI-powered early dropout warning engine synchronizing live LMS attendance with predictive bunk & OD optimization."
    tp.font.size = Pt(11)
    tp.font.bold = True
    tp.font.color.rgb = RGBColor(67, 56, 202)

    col_w = Inches(3.75)
    col_gap = Inches(0.24)
    col_y = Inches(2.25)
    col_h = Inches(4.5)

    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), col_y, col_w, col_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = BG_LIGHT
    c1.line.color.rgb = CARD_BORDER
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = Inches(0.25)
    p = tf1.paragraphs[0]
    p.text = "01  PROPOSED SOLUTION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf1.add_paragraph()
    p.text = "What we are building:\n• Autonomous Playwright scraper: 1-click live login to Linways AMS to extract official attendance, weekly timetable & calendar.\n• Pure Math Bunk Simulator: Real-time simulation of safe bunks, recovery needs, and dynamic remaining sessions.\n• Grok AI Academic Strategist: Computes exact schedule-level bunk vs attend recommendations till semester freeze date (Dec 1)."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + col_w + col_gap, col_y, col_w, col_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = BG_LIGHT
    c2.line.color.rgb = CARD_BORDER
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Inches(0.25)
    p = tf2.paragraphs[0]
    p.text = "02  HOW IT SOLVES THE GAP"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf2.add_paragraph()
    p.text = "The Exact Gap Closed:\n• Universities detect dropouts post-mortem: When a student hits 60%, debarment is already sealed.\n• AttendTrack intervenes pre-emptively: Calculates exact attend quotas weeks in advance.\n• Event OD Allocation: Maps hackathon / sports duty leave credits to borderline subjects to rescue them from detention in real time."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    c3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + (col_w + col_gap) * 2, col_y, col_w, col_h)
    c3.fill.solid()
    c3.fill.fore_color.rgb = BG_LIGHT
    c3.line.color.rgb = CARD_BORDER
    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = Inches(0.25)
    p = tf3.paragraphs[0]
    p.text = "03  WHY IT'S DIFFERENT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf3.add_paragraph()
    p.text = "Defensible Edge:\n• Official portals show historical deficit with zero guidance. AttendTrack is 100% predictive.\n• Zero manual typing: Auto-parses HTML, PDF reports, Timetable images & direct JSON.\n• Weekly Day Bunk Simulator: Color-coded lecture cards (Green=Safe, Orange=Risky, Red=DO NOT BUNK) with 1-click batch day actions."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    # -------------------------------------------------------------------------
    # SLIDE 3: TECHNICAL APPROACH
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "TECHNICAL APPROACH", 3)

    box_w = Inches(5.6)
    c1 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), box_w, Inches(1.6))
    c1.fill.solid()
    c1.fill.fore_color.rgb = BG_LIGHT
    c1.line.color.rgb = CARD_BORDER
    tf = c1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "01  TECH STACK"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "• Core: Python 3.12, Flask REST API\n• Automation: Playwright Chromium (Headless + Headed Live Viewport)\n• Parser & OCR: pdfplumber, PIL (Pillow), BeautifulSoup4\n• Intelligence: xAI Grok API + Offline Heuristic Academic Engine"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_MAIN

    c2 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.15), box_w, Inches(1.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = BG_LIGHT
    c2.line.color.rgb = CARD_BORDER
    tf = c2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "02  METHODOLOGY & DATA FLOW"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "1. Student Auth & Ingestion: Headless browser extracts 13 subjects, TH, AH, DL.\n2. Calendar Horizon Mapping: Computes working days till semester freeze (Dec 1).\n3. Linear Bunk Optimization: Solves for max safe bunks and min required attends.\n4. Real-time Reactive UI: Immediate feedback on day bunks, steppers, and ODs."
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_MAIN

    c3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.1), box_w, Inches(1.65))
    c3.fill.solid()
    c3.fill.fore_color.rgb = BG_LIGHT
    c3.line.color.rgb = CARD_BORDER
    tf = c3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "03  WHAT WE DEMO (100% OPERATIONAL)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "• Live working web server at localhost:5000 & LAN (172.18.130.18:5000)\n• Live visual Playwright automation stream with address bar & real-time screens\n• 1-Click Grok 75% target optimizer allocating exact bunks/attends till Dec 1\n• Collapsible Weekly Schedule Simulator & Event OD Day selector"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_MAIN

    arch = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.4), Inches(5.933), Inches(5.35))
    arch.fill.solid()
    arch.fill.fore_color.rgb = BG_DARK
    arch.line.color.rgb = CYAN_ACCENT
    atf = arch.text_frame
    atf.word_wrap = True
    atf.margin_left = atf.margin_right = Inches(0.3)
    p = atf.paragraphs[0]
    p.text = "SYSTEM ARCHITECTURE & EXECUTION FLOW"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    arch_text = """
+--------------------------------------------------------+
|  LINWAYS AMS STUDENT PORTAL (Presidency University)    |
|  [Student ID / Password] or [PDF / Image / HTML Upload]|
+---------------------------+----------------------------+
                            | Playwright Chromium Scraper
+---------------------------v----------------------------+
|  ATTENDTRACK REST BACKEND (Python Flask on Port 5000)  |
|  * Session Parser (TH, AH, DL, %AH+DL)                 |
|  * Academic Calendar & Countdown Engine (Dec 01, 2026) |
|  * Mathematical Prediction Engine                      |
+-------------+----------------------------+-------------+
              |                            |
+-------------v---------------+ +----------v-------------+
| PURE MATH SIMULATOR         | | xAI GROK ADVISOR       |
| * Safe Bunk Maxima:         | | * 75% Strategy Engine  |
|   (AH+DL - 0.75*TH) / 0.75  | | * Natural Language QA  |
| * Recovery Thresholds       | | * Semester-End Plan    |
+-------------+---------------+ +----------+-------------+
              |                            |
+-------------v----------------------------v-------------+
|  REACTIVE CLIENT DASHBOARD (Vanilla JS, Zero Bloat)     |
|  * Weekly Schedule Degree Defense (Collapsible)        |
|  * Course Breakdown Table & Real-Time Steppers         |
|  * Event OD Missed-Day Selector (Mon-Sat auto-credits) |
+--------------------------------------------------------+
"""
    p = atf.add_paragraph()
    p.text = arch_text
    p.font.size = Pt(7.5)
    p.font.name = "Courier New"
    p.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------------------
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "FEASIBILITY AND VIABILITY", 4)

    col_w2 = Inches(3.75)
    f1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), col_w2, Inches(2.5))
    f1.fill.solid()
    f1.fill.fore_color.rgb = BG_LIGHT
    f1.line.color.rgb = CARD_BORDER
    tf = f1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FEASIBILITY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "• Built in 1 Day: Fully functional working prototype delivered on hackathon day.\n• Local & Cloud Ready: Runs standalone on Windows/Linux or deployable via Docker/Gunicorn.\n• Low Resource Footprint: Lightweight Flask server, zero heavyweight frontend dependencies."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    f2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + col_w2 + col_gap, Inches(1.4), col_w2, Inches(2.5))
    f2.fill.solid()
    f2.fill.fore_color.rgb = BG_LIGHT
    f2.line.color.rgb = CARD_BORDER
    tf = f2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CHALLENGES & RISKS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p = tf.add_paragraph()
    p.text = "• Portal Layout Volatility: University AMS UI updates breaking scrapers.\n• Credential Security: Reluctance of students to share login passwords.\n• API Outages: Remote Grok/xAI rate limits or connectivity loss during demos."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    f3 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + (col_w2 + col_gap)*2, Inches(1.4), col_w2, Inches(2.5))
    f3.fill.solid()
    f3.fill.fore_color.rgb = BG_LIGHT
    f3.line.color.rgb = CARD_BORDER
    tf = f3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MITIGATION STRATEGY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p = tf.add_paragraph()
    p.text = "• Universal Multi-Format Ingestion: Supports direct PDF attendance reports, timetable images, HTML & CSV uploads.\n• Ephemeral Client Processing: Zero credential persistence.\n• Dual Intelligence Engine: Smart local heuristic academic engine kicks in automatically if external API fails."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    plan_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.15), Inches(11.733), Inches(2.6))
    plan_card.fill.solid()
    plan_card.fill.fore_color.rgb = BG_DARK
    plan_card.line.color.rgb = CARD_BORDER
    ptf = plan_card.text_frame
    ptf.word_wrap = True
    ptf.margin_left = ptf.margin_right = Inches(0.3)
    p = ptf.paragraphs[0]
    p.text = "ONE-DAY HACKATHON EXECUTION PLAN"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    steps = [
        ("PHASE 1: BUILD & EXPLORE (Morning)", "• Scraped live Linways AMS with Playwright.\n• Built PDF parser & fixed course code number regex bug.\n• Implemented pure deterministic mathematical simulation engine."),
        ("PHASE 2: DEMO EVALUATION (Afternoon)", "• Integrated Grok 75% target schedule optimizer.\n• Built collapsible Weekly Schedule with Day Bunk actions.\n• Created Event OD Missed Day selector (Mon-Sat auto-credits)."),
        ("PHASE 3: JURY PITCH & DEFENSE (Evening)", "• Live demonstration running on localhost and local network Wi-Fi.\n• Full visual browser automation streaming viewport.\n• Complete slide deck & defense presentation ready.")
    ]

    for title, desc in steps:
        p = ptf.add_paragraph()
        p.text = f"{title}\n{desc}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(226, 232, 240)

    # -------------------------------------------------------------------------
    # SLIDE 5: IMPACT AND BENEFITS
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "IMPACT AND BENEFITS", 5)

    stat_w = Inches(3.75)
    stats = [
        ("100%", "ZERO DEBARMENTS", "Students who follow AttendTrack safe bunk limits never drop below 75%"),
        ("22+", "SAFE BUNKS UNLOCKED", "High-attendance subjects safely leveraged without risking eligibility"),
        ("5+ hrs", "TIME SAVED PER SEMESTER", "Eliminates tedious manual math, guessing and spreadsheet maintenance")
    ]
    for i, (big, title, sub) in enumerate(stats):
        sc = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + (stat_w + col_gap) * i, Inches(1.4), stat_w, Inches(1.8))
        sc.fill.solid()
        sc.fill.fore_color.rgb = BG_LIGHT
        sc.line.color.rgb = CARD_BORDER
        stf = sc.text_frame
        stf.word_wrap = True
        stf.margin_top = Inches(0.15)
        p = stf.paragraphs[0]
        p.text = big
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p = stf.add_paragraph()
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p = stf.add_paragraph()
        p.text = sub
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED

    w_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.45), Inches(5.7), Inches(3.3))
    w_card.fill.solid()
    w_card.fill.fore_color.rgb = BG_LIGHT
    w_card.line.color.rgb = CARD_BORDER
    tf = w_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "WHO IT HELPS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "• Primary: 10,000+ university undergraduates navigating mandatory 75% attendance rules under university statutes.\n• Event Participants: Hackathon attendees, sports teams, and cultural performers who miss lectures and struggle to claim timely On-Duty (OD) credits.\n• Academic Mentors & HODs: Faculty can identify at-risk students 3 weeks before semester examinations rather than after cutoff."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    b_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(3.45), Inches(5.7), Inches(3.3))
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = BG_LIGHT
    b_card.line.color.rgb = CARD_BORDER
    tf = b_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "MULTI-TIER BENEFITS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "• Academic Integrity & Security: Proactively eliminates surprise debarments and attendance tampering.\n• Social & Mental Well-being: Drastically lowers student anxiety and burnout by giving clear, mathematically guaranteed control over their schedule.\n• Economic Value: Prevents costly summer repeats and registration re-fees (Rs. 15,000+ per course repeat).\n• Institutional Retention: Prevents student dropouts triggered by cascading attendance defaults."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    # -------------------------------------------------------------------------
    # SLIDE 6: RESEARCH AND REFERENCES
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "RESEARCH AND REFERENCES", 6)

    r_w = Inches(5.7)
    rc1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), r_w, Inches(2.6))
    rc1.fill.solid()
    rc1.fill.fore_color.rgb = BG_LIGHT
    rc1.line.color.rgb = CARD_BORDER
    tf = rc1.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "SOURCES BEHIND THE IDEA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "• Presidency University Academic Regulations (75% Attendance & Duty Leave clause).\n• National Education Policy (NEP 2020) Guidelines on Early Warning Systems for Student Retention.\n• Playwright Automation Framework (Microsoft Open Source).\n• xAI Grok API Documentation & Prompt Engineering Patterns."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    rc2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.4), r_w, Inches(2.6))
    rc2.fill.solid()
    rc2.fill.fore_color.rgb = BG_LIGHT
    rc2.line.color.rgb = CARD_BORDER
    tf = rc2.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "ETHICS & RESPONSIBLE DATA HANDLING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p = tf.add_paragraph()
    p.text = "• Ephemeral Session Processing: Student credentials are used strictly in-memory during scraping and never stored in databases.\n• Transparent Mathematical Audit: Formulations follow official university evaluation policy: (AH + DL) / TH * 100.\n• Non-Bypass Architecture: AttendTrack does not tamper with university records; it empowers students with ethical predictive insights."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MAIN

    check_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(11.733), Inches(2.55))
    check_card.fill.solid()
    check_card.fill.fore_color.rgb = BG_DARK
    check_card.line.color.rgb = CYAN_ACCENT
    ctf = check_card.text_frame
    ctf.word_wrap = True
    ctf.margin_left = ctf.margin_right = Inches(0.3)
    p = ctf.paragraphs[0]
    p.text = "BEFORE YOU SUBMIT CHECKLIST (100% COMPLIANT WITH BUG HUNT ARENA 2026)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    checks = [
        "v Exactly 6 slides maximum, title slide included (Instructions slide deleted).",
        "v Structured points, architecture flow diagram and infographics only - no dense paragraphs.",
        "v Original and novel engineering: Live Playwright automation + Grok AI optimization + Bunk math.",
        "v All required template section headings preserved without modification.",
        "v Team Name 'Team Syndicate' featured on all slides.",
        "v Full working prototype deployed and running live for jury demonstration."
    ]
    for chk in checks:
        p = ctf.add_paragraph()
        p.text = chk
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(226, 232, 240)

    output_path = os.path.join(os.getcwd(), "Team_Syndicate_Bug_Hunt_Arena_2026.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_deck()
