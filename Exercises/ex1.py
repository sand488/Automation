from playwright.sync_api import sync_playwright


def test_beta():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto("https://b2bbeta.akbartravelsonline.com")

        print("BETA URL:", page.url)
        print("BETA Title:", page.title())

        browser.close()
