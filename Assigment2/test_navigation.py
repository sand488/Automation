from playwright.sync_api import sync_playwright


def test_google_navigation():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        # Open Google
        page.goto("https://www.google.com")

        # Fill Google search box
        page.locator("@id//gws-output-pages-elements-homepage_additional_languages__als[name='q']").fill("Playwright Python")

        # Press Enter
        page.locator("textarea[name='q']").press("Enter")

        # Wait for search results page
        page.wait_for_load_state("domcontentloaded")

        # Print page title   
        print("Title:", page.title())

        # Close browser
        browser.close()