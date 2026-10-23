from playwright.sync_api import sync_playwright


def test_qa():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto("https://b2bdesk.akbartravelsonline.com")

        print("QA URL:", page.url)
        print("QA Title:", page.title())

        browser.close()
