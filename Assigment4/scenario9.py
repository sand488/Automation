import pytest
from playwright.async_api import expect

from helpers import (
    search_amazon,
    find_product_card,
)


# Scenario 9: Add to Cart Only When Available

@pytest.mark.asyncio
@pytest.mark.amazon
async def test_add_to_cart_only_when_available(
    amazon_page,
    product_keyword,
):
    page = amazon_page

    # Step 1: Search for the product
    await search_amazon(page, product_keyword)

    # Step 2: Find the matching product card
    card = await find_product_card(page, product_keyword)

    # Step 3: Locate and open the product in the same tab
    product_link = card.locator("a:has(h2)").first

    await expect(product_link).to_be_visible(timeout=10000)

    await product_link.evaluate(
        "(element) => element.removeAttribute('target')"
    )
    await product_link.click()

    # Step 4: Verify that the product page has opened
    product_title = page.locator("span#productTitle")

    await expect(product_title).to_be_visible(timeout=20000)

    title = " ".join(
        (await product_title.inner_text()).split()
    )

    print("Selected product:", title)

    # Step 5: Check whether Add to Cart is available
    add_button = page.locator("#add-to-cart-button")

    if not await add_button.is_visible():
        pytest.skip(
            f"Add to Cart is not visible for {title!r}."
        )

    if not await add_button.is_enabled():
        pytest.skip(
            f"Add to Cart is disabled for {title!r}."
        )

    # Step 6: Add the product to the cart
    await add_button.click()

    print("Add to Cart clicked successfully.")

    # Step 7: Navigate to the cart
    cart_link = page.locator("#nav-cart")

    await expect(cart_link).to_be_visible(timeout=15000)
    await cart_link.click()

    await page.wait_for_load_state(
        "domcontentloaded",
        timeout=30000,
    )

    # Step 8: Verify the product appears in the cart
    cart_text = " ".join(
        (await page.locator("body").inner_text()).split()
    )

    product_words = title.split()
    search_term = " ".join(product_words[:3])

    assert search_term.casefold() in cart_text.casefold(), (
        f"Product was not found in the cart. "
        f"Expected title: {title!r}"
    )

    print("Cart validated successfully.")
    print("Test stops before checkout or purchase.")