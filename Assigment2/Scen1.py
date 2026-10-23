
# Scenario 1: DemoWebShop – Registration Form and Add to Cart

from playwright.sync_api import expect


def test_get_by_label(page):
    """Fill registration form fields using get_by_label()."""

    # Step 1: Open DemoWebShop
    page.goto("https://demowebshop.tricentis.com/")

    # Step 2: Open registration page
    page.get_by_text("Register", exact=True).click()

    # Step 3: Select gender
    page.get_by_label("Female", exact=True).check()

    # Step 4: Fill personal details
    page.get_by_label("First name:", exact=True).fill("Sandhya")
    page.get_by_label("Last name:", exact=True).fill("Bhaskarankurup")
    page.get_by_label("Email:", exact=True).fill(
        "sandyabhaskar1@gmail.com"
    )

    # Step 5: Fill both password fields
    page.get_by_label("Password:", exact=True).fill("san89999")
    page.get_by_label("Confirm password:", exact=True).fill("san89999")

    # Step 6: Verify that the fields contain the entered values
    expect(
        page.get_by_label("First name:", exact=True)
    ).to_have_value("Sandhya")

    expect(
        page.get_by_label("Last name:", exact=True)
    ).to_have_value("Bhaskarankurup")

    print("PASS: Registration form fields populated successfully.")


def test_demowebshop_find_product_add_to_cart(page):
    """Find Computing and Internet and add it to the cart."""

    product_name = "Computing and Internet"

    # Step 1: Open the Books category
    page.goto("https://demowebshop.tricentis.com/books")

    # Step 2: Locate the product
    product = page.locator(
        "//div[contains(@class,'product-item')]"
        f"[.//a[normalize-space()='{product_name}']]"
    )

    expect(product).to_be_visible(timeout=15000)

    print("\nProduct found:", product_name)

    # Step 3: Locate Add to Cart inside the selected product
    add_to_cart = product.locator(
        "input.button-2.product-box-add-to-cart-button"
    )

    expect(add_to_cart).to_be_visible()
    add_to_cart.click()

    # Step 4: Verify the success notification
    notification = page.locator(".bar-notification")

    expect(notification).to_contain_text(
        "The product has been added",
        timeout=10000
    )

    print(f"PASS: '{product_name}' added to cart successfully.")
