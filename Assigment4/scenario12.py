import pytest
from playwright.async_api import expect

from helpers import (
    search_amazon,
    find_product_card,
)


# Scenario 12: Add to Cart and Stop Before Purchase

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

    # Step 3: Locate the product link
    product_link = card.locator("a:has(h2)").first

    await expect(product_link).to_be_visible(timeout=10000)

    target = await product_link.get_attribute("target")

    # Step 4: Open the product page and keep it available
    if target == "_blank":
        async with page.expect_popup() as popup_info:
            await product_link.click()

        product_page = await popup_info.value
    else:
        await product_link.click()
        product_page = page

    # Step 5: Verify the product details page
    product_title = product_page.locator("span#productTitle")

    await expect(product_title).to_be_visible(timeout=20000)

    selected_title = " ".join(
        (await product_title.inner_text()).split()
    )

    print("Selected product:", selected_title)

    # Step 6: Check Add to Cart availability
    add_button = product_page.locator("#add-to-cart-button")

    if not await add_button.is_visible():
        pytest.skip(
            f"Add to Cart is not visible for {selected_title!r}. "
            "No cart action was performed."
        )

    if not await add_button.is_enabled():
        pytest.skip(
            f"Add to Cart is disabled for {selected_title!r}. "
            "The product may be unavailable."
        )

    # Step 7: Add the product to the cart
    await add_button.click()

    print("Add to Cart clicked successfully.")

    # Step 8: Navigate to the cart
    cart_link = product_page.locator("#nav-cart")

    await expect(cart_link).to_be_visible(timeout=15000)
    await cart_link.click()

    await product_page.wait_for_load_state(
        "domcontentloaded",
        timeout=30000,
    )

    # Step 9: Verify the product appears in the cart
    cart_text = " ".join(
        (await product_page.locator("body").inner_text()).split()
    )

    first_words = " ".join(selected_title.split()[:3])

    assert (
        selected_title.casefold() in cart_text.casefold()
        or first_words.casefold() in cart_text.casefold()
    ), (
        f"Selected product was not found in the cart. "
        f"Product: {selected_title!r}"
    )

    print("Cart validated successfully.")
    print("Test intentionally stops before checkout or purchase.")