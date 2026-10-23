
# Scenario 8: Amazon – Navigation Menu Subcategories

from playwright.sync_api import sync_playwright, expect


def test_amazon_navigation_subcategories():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Open Amazon India
            page.goto(
                "https://www.amazon.in/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Step 2: Open the hamburger menu
            page.locator(
                "//a[@id='nav-hamburger-menu']"
            ).click()

            # Step 3: Locate the navigation menu
            menu = page.get_by_role("dialog")

            # Step 4: Locate the main heading
            heading_name = "Digital Content and Devices"

            heading = menu.get_by_role(
                "heading",
                name=heading_name,
                exact=True
            )

            expect(heading).to_be_visible(timeout=10000)

            print("\nMain Heading:", heading_name)

            # Step 5: Locate the region using its visible text
            heading_section = menu.get_by_role(
                "region"
            ).filter(has_text=heading_name)

            expect(
                heading_section
            ).to_be_visible(timeout=10000)

            # Step 6: Find and print all subcategories
            subcategories = heading_section.get_by_role("button")

            count = subcategories.count()

            print("\nSUBCATEGORIES")

            for i in range(count):
                subcategory_name = (
                    subcategories.nth(i).inner_text().strip()
                )

                if subcategory_name:
                    print(f"{i + 1}. {subcategory_name}")

            # Step 7: Select Amazon Music
            required_subcategory = "Amazon Music"

            amazon_music = heading_section.get_by_role(
                "button",
                name=required_subcategory,
                exact=True
            )

            expect(amazon_music).to_be_visible()
            amazon_music.click()

            print(
                f"\nPASS: '{required_subcategory}' selected."
            )

        finally:
            # Step 8: Close the browser
            browser.close()
