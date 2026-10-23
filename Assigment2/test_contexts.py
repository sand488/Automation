from playwright.sync_api import sync_playwright


def test_two_contexts():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        context1 = browser.new_context()
        context2 = browser.new_context()

        page1 = context1.new_page()
        page2 = context2.new_page()

        page1.goto("https://www.google.com")
        page2.goto("https://www.google.com")

        print("Context 1:", page1.title())
        print("Context 2:", page2.title())

        context1.close()
        context2.close()
        browser.close()