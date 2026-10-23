
from playwright.sync_api import sync_playwright

def test_scenario_1():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        try:
            page = browser.new_page()
            page.goto("https://example.com")
            print(page.title())
        finally:
            browser.close()