#Scenario 1: DemoWebShop – Product Name to Add to Cart
from playwright.sync_api import sync_playwright, expect


def test_demowebshop_add_book_to_cart():

    product_name = "Health Book"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()

            # Open DemoWebShop
            page.goto("https://demowebshop.tricentis.com/")

            # Navigate to Books
            page.locator(
                "//ul[@class='top-menu']//a[normalize-space()='Books']"
            ).click()

            # Find the product dynamically by name
            product = page.locator(
                f"//div[contains(@class,'product-item')]"
                f"[.//h2//a[normalize-space()='{product_name}']]"
            )

            expect(product).to_be_visible()

            # Click Add to Cart within the selected product
            product.locator(
                "xpath=.//input[contains(@class,'product-box-add-to-cart-button')]"
            ).click()

            # Verify the success notification
            expect(page.locator(".bar-notification")).to_contain_text(
                "The product has been added"
            )

            # Open Shopping Cart
            page.locator(
                "//span[@class='cart-label' and normalize-space()='Shopping cart']"
            ).click()

            # Verify the product appears in the cart
            cart_product = page.locator(
                f"//table[contains(@class,'cart')]"
                f"//a[normalize-space()='{product_name}']"
            )

            expect(cart_product).to_be_visible()

            print(
                f"'{product_name}' has been successfully added to the cart."
            )

        finally:
            browser.close()