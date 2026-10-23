
# Scenario 9: DemoWebShop – Product Details

from playwright.sync_api import sync_playwright, expect


def test_demowebshop_product_details():

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

            # Step 3: Select Health Book
            product_name = "Health Book"

            product_link = page.locator(
                f"//h2/a[normalize-space()='{product_name}']"
            )

            expect(product_link).to_be_visible(timeout=15000)
            product_link.click()

            page.wait_for_load_state("domcontentloaded")

            # Step 4: Verify product name
            product_title = page.locator(
                "//div[contains(@class,'product-name')]"
                f"//h1[normalize-space()='{product_name}']"
            )

            expect(product_title).to_be_visible()

            print("\n========== PRODUCT DETAILS ==========")
            print("Product Name :", product_title.inner_text().strip())

            # Step 5: Get product price
            price = page.locator(
                "//div[contains(@class,'product-price')]"
                "//span[contains(@class,'price')]"
            ).first

            expect(price).to_be_visible()

            print("Product Price:", price.inner_text().strip())

            # Step 6: Locate Add to Cart
            add_to_cart = page.locator(
                "#product-details-form input.add-to-cart-button"
            )

            expect(add_to_cart).to_be_visible()

            print("Add to Cart  : Available")

            # Step 7: Add product to cart
            add_to_cart.click()

            # Step 8: Verify success notification
            notification = page.locator("#bar-notification")

            expect(notification).to_contain_text(
                "The product has been added to your shopping cart",
                timeout=10000
            )

            print("Add to Cart  : Product added successfully")

            # Step 9: Open the Shopping Cart
            cart_link = page.get_by_role(
                "link",
                name="Shopping cart",
                exact=True
            )

            expect(cart_link).to_be_visible()
            cart_link.click()

            # Step 10: Verify product in cart
            cart_product = page.locator(
                "//a[contains(@class,'product-name') "
                f"and normalize-space()='{product_name}']"
            )

            expect(cart_product).to_be_visible(timeout=15000)

            print("Cart Status  : Product added successfully")
            print("\nTEST PASSED")

        finally:
            browser.close()
