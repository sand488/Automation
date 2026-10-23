# Scenario 3: DemoWebShop – Select Product by Price

from playwright.sync_api import sync_playwright, expect


def test_demowebshop_select_product_by_price():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://demowebshop.tricentis.com/")
            page.wait_for_load_state("domcontentloaded")

            page.locator(
                "//ul[@class='top-menu']//a[normalize-space()='Books']"
            ).click()

            # Select product by name and current price
            product_name = "Computing and Internet"
            product_price = "10.00"

            product = page.locator(
                f"//div[contains(@class,'product-item')]"
                f"[.//h2/a[normalize-space()='{product_name}']]"
            )

            expect(product).to_be_visible()

            # Verify the current price
            prices = product.locator(".prices .price")
            actual_prices = [
                price.strip() for price in prices.all_inner_texts()
            ]

            print("Product Name:", product_name)
            print("Displayed Prices:", actual_prices)

            assert product_price in actual_prices, (
                f"Expected price {product_price} not found. "
                f"Actual prices: {actual_prices}"
            )

            print("Verified Current Price:", product_price)

            # Locate Add to Cart within the selected product
            add_to_cart = product.locator(
                "xpath=.//input[@value='Add to cart']"
            )

            expect(add_to_cart).to_be_visible()
            add_to_cart.click()

            # Verify that the product was added successfully
            expect(page.locator("#bar-notification")).to_contain_text(
                "The product has been added to your shopping cart"
            )

            # Open Shopping Cart
            page.locator(
                "//span[@class='cart-label' "
                "and normalize-space()='Shopping cart']"
            ).click()

            # Verify the product is in the cart
            cart_product = page.locator(
                   f"//a[contains(@class,'product-name') "
                   f"and normalize-space()='{product_name}']"
                   )

            expect(cart_product).to_be_visible()

            print(
                f"PASS: {product_name} "
                f"({product_price}) added to cart successfully."
            )

        finally:
            browser.close()
