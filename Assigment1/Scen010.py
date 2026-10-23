
# Scenario 10: Amazon – Select Samsung Product from Search Results

from urllib.parse import urljoin
from playwright.sync_api import sync_playwright, expect


def test_amazon_select_product_from_search_results():

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

            # Step 2: Search for Samsung Galaxy S26 Ultra
            search_box = page.locator(
                "#twotabsearchtextbox"
            )

            search_box.fill(
                "Samsung Galaxy S26 Ultra 5G Cobalt Violet 256GB"
            )

            page.locator(
                "#nav-search-submit-button"
            ).click()

            # Step 3: Wait for search results
            page.wait_for_url("**/s?*", timeout=30000)

            # Step 4: Locate the exact product title
            product_heading = page.locator(
                "//h2[contains(@aria-label,'Galaxy S26 Ultra 5G') "
                "and contains(@aria-label,'Cobalt Violet') "
                "and contains(@aria-label,'256GB Storage')]"
            ).first

            expect(
                product_heading
            ).to_be_visible(timeout=20000)

            actual_title = product_heading.inner_text().strip()

            print("\n========== SELECTED PRODUCT ==========")
            print("Product Title:", actual_title)

            # Step 5: Locate the product card
            product_card = product_heading.locator(
                "xpath=ancestor::div"
                "[@data-component-type='s-search-result'][1]"
            )

            expect(product_card).to_be_visible()

            # Step 6: Verify product image
            product_image = product_card.locator(
                "img.s-image"
            ).first

            expect(product_image).to_be_visible(timeout=10000)

            print("Product Image: Available")

            # Step 7: Extract product price
            price = product_card.locator(
                "span.a-price:not(.a-text-price) "
                "span.a-offscreen"
            ).first

            if price.count() > 0:
                print("Product Price:", price.inner_text().strip())
            else:
                print("Product Price: Not available")

            # Step 8: Get the product details URL
            product_link = product_heading.locator(
                "xpath=ancestor::a[1]"
            )

            expect(product_link).to_be_visible()

            product_href = product_link.get_attribute("href")

            assert product_href, (
                "Product details URL was not found."
            )

            product_url = urljoin(
                "https://www.amazon.in/",
                product_href
            )

            print("Product URL:", product_url)

            # Step 9: Navigate directly to the product details page
            page.goto(
                product_url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Step 10: Verify product details
            details_title = page.locator("span#productTitle")

            expect(
                details_title
            ).to_be_visible(timeout=30000)

            actual_details_title = details_title.inner_text().strip()

            print("\n========== PRODUCT DETAILS ==========")
            print("Details Title:", actual_details_title)

            # Verify the selected Samsung model and variant
            assert "Galaxy S26 Ultra 5G" in actual_details_title
            assert "Cobalt Violet" in actual_details_title
            assert "256GB Storage" in actual_details_title

            print("\nPASS: Correct Samsung product details displayed.")

        finally:
            browser.close()
