
import re
from playwright.sync_api import sync_playwright, expect


def normalize(text):
    """Remove spaces and special characters for comparison."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def test_amazon_product_name_and_price():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Open Amazon search results directly
            page.goto(
                "https://www.amazon.in/s?k=Nothing+Phone+2",
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Step 2: Wait for search results
            page.wait_for_selector(
                "div[data-component-type='s-search-result']",
                timeout=30000
            )

            # Step 3: Locate actual product cards
            product_cards = page.locator(
                "div[data-component-type='s-search-result']"
                "[data-asin]:not([data-asin=''])"
            )

            print("\n========== AMAZON SEARCH RESULTS ==========")
            print("Product cards found:", product_cards.count())

            expected_name = normalize("Nothing Phone 2")
            selected_product = None
            actual_product_name = ""

            # Step 4: Find the correct product
            for i in range(product_cards.count()):
                card = product_cards.nth(i)

                # Check different title locators
                title_candidates = []

                for selector in [
                    "h2 a span",
                    "h2 a",
                    "h2",
                    "span.a-size-medium.a-color-base.a-text-normal",
                    "span.a-size-base-plus.a-color-base.a-text-normal"
                ]:
                    texts = card.locator(selector).all_inner_texts()
                    title_candidates.extend(
                        text.strip() for text in texts if text.strip()
                    )

                print(f"\nCard {i + 1} title candidates: {title_candidates}")

                # Find a title that matches the requested product
                for title in title_candidates:
                    if expected_name in normalize(title):
                        selected_product = card
                        actual_product_name = title
                        break

                if selected_product is not None:
                    break

            # Step 5: Verify product was found
            assert selected_product is not None, (
                "Nothing Phone 2 was not found in the product titles. "
                "Check the printed title candidates and Amazon results."
            )

            expect(selected_product).to_be_visible()

            print("\n========== SELECTED PRODUCT ==========")
            print("Product Name:", actual_product_name)

            # Step 6: Extract the displayed selling price
            price_locator = selected_product.locator(
                "span.a-price:not(.a-text-price) span.a-offscreen"
            ).first

            assert price_locator.count() > 0, (
                "The selected product does not have a visible price "
                "in the current search results."
            )

            actual_price = price_locator.inner_text().strip()

            print("Product Price:", actual_price)

            # Step 7: Verify product name
            assert expected_name in normalize(actual_product_name), (
                "Product name verification failed."
            )

            print("\nProduct name verification PASSED.")
            print("Product price extraction PASSED.")

        finally:
            browser.close()
