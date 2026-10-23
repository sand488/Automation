
import re
from playwright.sync_api import sync_playwright, expect


def test_demowebshop_product_name_and_rating():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Open DemoWebShop
            page.goto(
                "https://demowebshop.tricentis.com/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Step 2: Navigate to Books
            page.locator(
                "//ul[@class='top-menu']//a[normalize-space()='Books']"
            ).click()

            # Step 3: Locate Health Book
            product_name = "Health Book"

            product = page.locator(
                "//div[contains(@class,'product-item')]"
                f"[.//h2/a[normalize-space()='{product_name}']]"
            )

            expect(product).to_be_visible(timeout=15000)

            # Step 4: Get product name
            # CSS selector: h2 a
            actual_product_name = product.locator(
                "h2 a"
            ).inner_text().strip()

            print("\n========== PRODUCT DETAILS ==========")
            print("Product Name:", actual_product_name)

            assert actual_product_name == product_name, (
                f"Expected '{product_name}', "
                f"but found '{actual_product_name}'"
            )

            # Step 5: Open the product details page
            product.locator("h2 a").click()
            page.wait_for_load_state("domcontentloaded")

            # Step 6: Verify the product details page
            expect(page.locator("h1")).to_contain_text(
                product_name,
                timeout=15000
            )

            # Step 7: Locate the rating bar
            rating_bar = page.locator(
                ".product-review-overview .rating div"
            ).first

            if rating_bar.count() == 0:
                rating_bar = page.locator(
                    ".product-review-box .rating div"
                ).first

            assert rating_bar.count() > 0, (
                "Product rating element was not found."
            )

            # Step 8: Calculate rating from star-bar width
            style = rating_bar.get_attribute("style") or ""

            match = re.search(
                r"width\s*:\s*([\d.]+)%",
                style
            )

            assert match, (
                f"Could not extract rating from style: {style}"
            )

            rating_percentage = float(match.group(1))
            rating = round(rating_percentage / 20, 1)

            print("Product Rating:", rating, "/ 5")

            # Step 9: Verify rating
            assert 0 <= rating <= 5, (
                f"Invalid product rating: {rating}"
            )

            print("\nProduct name verification PASSED.")
            print("Product rating verification PASSED.")

        finally:
            # Step 10: Close browser
            browser.close()
