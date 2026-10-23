import pytest
from playwright.async_api import expect

from helpers import search_amazon, find_product_card, card_title


# Scenario 4: Add Product to Cart and Stop Before Purchase

@pytest.mark.asyncio
@pytest.mark.amazon
async def test_cart_journey_stops_before_purchase(
    amazon_page,
    product_keyword,
):
    page = amazon_page

    # Step 1: Search for the product
    await search_amazon(page, product_keyword)

    # Step 2: Find the matching product card
    card = await find_product_card(page, product_keyword)
    selected_title = await card_title(card)

    print("Selected product:", selected_title)

    # Step 3: Open the product page and keep it open
    product_link = card.locator("a:has(h2)").first

    await expect(product_link).to_be_visible(timeout=10000)

    target = await product_link.get_attribute("target")

    if target == "_blank":
        async with page.expect_popup() as popup_info:
            await product_link.click()

        product_page = await popup_info.value
    else:
        await product_link.click()
        product_page = page

    # Step 4: Verify the product details page
    product_title = product_page.locator("span#productTitle")

    await expect(product_title).to_be_visible(timeout=20000)

    actual_title = (await product_title.inner_text()).strip()

    print("Product details page:", actual_title)

    # Step 5: Check Add to Cart availability
    add_button = product_page.locator("#add-to-cart-button")

    if not await add_button.is_visible():
        pytest.skip(
            "Add to Cart is unavailable for this product/session. "
            "No cart action was performed."
        )

    if not await add_button.is_enabled():
        pytest.skip(
            "Add to Cart is disabled. The product may be unavailable."
        )

    # Step 6: Add the product to the cart
    await add_button.click()
    print("Add to Cart clicked.")

    # Step 7: Navigate to the cart
    cart_link = product_page.locator("#nav-cart")

    await expect(cart_link).to_be_visible(timeout=15000)
    await cart_link.click()

    await product_page.wait_for_load_state(
        "domcontentloaded",
        timeout=30000,
    )

    # Step 8: Verify the selected product appears in the cart
    cart_text = " ".join(
        (await product_page.locator("body").inner_text()).split()
    )

    if selected_title.casefold() not in cart_text.casefold():
        first_word = selected_title.split()[0]

        assert first_word.casefold() in cart_text.casefold(), (
            "Selected product was not found in the cart. "
            f"Product: {selected_title!r}"
        )

    print("Cart validated successfully.")
    print("Test intentionally stops before purchase/Place Order.")
