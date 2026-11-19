import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    print("Going to login page...")
    page.goto('https://presidencyuniversity.linways.com/ams/student/login', wait_until='networkidle')
    
    print("Filling credentials...")
    import os
    page.fill('#username', os.environ.get('STUDENT_USER', ''))
    page.fill('#password', os.environ.get('STUDENT_PASS', ''))
    page.click('#loginBtn')
    
    # Wait for response or navigation
    page.wait_for_timeout(5000)
    print("Current URL:", page.url)
    print("Page Title:", page.title())
    
    page.screenshot(path='dashboard.png', full_page=True)
    
    # Let's inspect all links and navigation items on the dashboard
    links = page.locator('a').all()
    print(f"Total links found: {len(links)}")
    for i, link in enumerate(links):
        text = link.inner_text().strip().replace('\n', ' ')
        href = link.get_attribute('href')
        if text or href:
            print(f"Link {i}: '{text}' -> {href}")
            
    browser.close()
