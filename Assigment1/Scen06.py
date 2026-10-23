
# Scenario 6: Amazon – Search Results

from playwright.sync_api import sync_playwright, expect


def test_amazon_search_result_book():

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

            # Step 2: Search for The Da Vinci Code
            search_box = page.locator(
                "//input[@id='twotabsearchtextbox']"
            )

            search_box.fill("The Da Vinci Code")

            page.locator(
                "//input[@id='nav-search-submit-button']"
            ).click()

            page.wait_for_load_state("domcontentloaded")

            # Step 3: Select the book by title
            book_title = "The Da Vinci Code"

            product = page.locator(
                "//div[@data-component-type='s-search-result']"
                f"[.//h2//span[contains("
                f"translate(normalize-space(),"
                f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                f"'abcdefghijklmnopqrstuvwxyz'),"
                f"'{book_title.lower()}')]]"
            ).first

            expect(product).to_be_visible(timeout=15000)

            # Step 4: Get the actual book title
            # CSS selector: h2 span
            title_locator = product.locator("h2 span").first

            actual_title = title_locator.inner_text().strip()

            print("\n========== BOOK DETAILS ==========")
            print("Expected Book:", book_title)
            print("Actual Book Title:", actual_title)

            # Step 5: Verify the book title
            assert book_title.lower() in actual_title.lower(), (
                f"Expected '{book_title}', "
                f"but found '{actual_title}'"
            )

            # Step 6: Locate the book price
            price = product.locator(
                "span.a-price:not(.a-text-price) "
                "span.a-offscreen"
            ).first

            if price.count() > 0:
                product_price = price.inner_text().strip()
                print("Book Price:", product_price)
            else:
                print("Price is not available.")

            # Step 7: Check Add to Cart availability
            add_to_cart = product.locator(
                "button:has-text('Add to cart'), "
                "input[value*='Add to Cart']"
            )

            if add_to_cart.count() > 0:
                expect(add_to_cart.first).to_be_visible()
                add_to_cart.first.click()

                print("Add to Cart clicked successfully.")
            else:
                print(
                    "Add to Cart is not available "
                    "in this search result."
                )

            print("\nBook title verification PASSED.")

        finally:
            # Step 8: Close the browser
            browser.close()
