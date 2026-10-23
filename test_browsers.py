import pytest
from playwright.sync_api import sync_playwright


@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_google_in_all_browsers(browser_name):

    with sync_playwright() as p:

        browser_type = getattr(p, browser_name)

        browser = browser_type.launch(headless=False)

        page = browser.new_page()

        page.goto("https://www.google.com")

        print(browser_name, "Title:", page.title())

        browser.close()