
# Scenario 7: DemoWebShop – Multiple Products

from playwright.sync_api import sync_playwright, expect


def test_demowebshop_multiple_products():

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

            # Step 3: Locate all products
            products = page.locator(
                "div.product-item"
            )

            expect(products.first).to_be_visible(timeout=15000)

            product_count = products.count()

            print("\n========== BOOKS AVAILABLE ==========")
            print("Total products:", product_count)

            # Step 4: Print all product names
            for i in range(product_count):

                product = products.nth(i)

                # CSS selector: h2 a
                title_locator = product.locator("h2 a")

                if title_locator.count() > 0:
                    product_name = title_locator.inner_text().strip()
                    print(f"{i + 1}. {product_name}")

            # Step 5: Select the target product
            target_product_name = "Health Book"

            target_product = page.locator(
                "//div[contains(@class,'product-item')]"
                f"[.//h2/a[normalize-space()='{target_product_name}']]"
            )

            expect(target_product).to_be_visible(timeout=15000)

            # Step 6: Locate Add to Cart for Health Book
            add_to_cart = target_product.locator(
                "input[value*='Add to cart']"
            )

            expect(add_to_cart).to_be_visible()
            add_to_cart.click()

            # Step 7: Verify the success notification
            notification = page.locator("#bar-notification")

            expect(notification).to_contain_text(
                "The product has been added to your shopping cart",
                timeout=10000
            )

            print(f"\n'{target_product_name}' added to cart.")

            # Step 8: Open Shopping Cart
            page.locator(
                "//span[@class='cart-label' "
                "and normalize-space()='Shopping cart']"
            ).click()

            # Step 9: Verify the product in the cart
            cart_product = page.locator(
                "//a[contains(@class,'product-name') "
                f"and normalize-space()='{target_product_name}']"
            )

            expect(cart_product).to_be_visible(timeout=15000)

            print(
                f"PASS: '{target_product_name}' "
                "is available in the cart."
            )

        finally:
            # Step 10: Close browser
            browser.close()