#Scenario 2: Amazon – Left Navigation Headings

from playwright.sync_api import sync_playwright, expect

def test_amazon_left_navigation_headings():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.amazon.in/")
        page.wait_for_load_state("domcontentloaded")

        menu = page.locator("//div[@id='hmenu-content']")

        headings = page.locator("xpath=.//div[contains(@class,'hmenu-title')]")

        count = headings.count()

        for i in range(count):
            heading = headings.nth(i).inner_text().strip()

            if heading:
                print(heading)

        browser.close()