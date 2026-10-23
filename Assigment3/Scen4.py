import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_drop(async_page):

    # Step 1: Open Amazon India
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    # Step 2: Search for bedsheets
    search_box = async_page.get_by_role(
        "searchbox",
        name="Search Amazon.in"
    )

    await expect(search_box).to_be_visible(timeout=20000)
    await search_box.fill("bead sheet king size")

    await async_page.locator("#nav-search-submit-button").click()
    await async_page.wait_for_timeout(3000)

    # Step 3: Locate the Add to Cart button
    add_to_cart = async_page.locator(
        "#a-autoid-3"
    ).get_by_role("button", name="Add to cart")

    await expect(add_to_cart).to_be_visible(timeout=20000)
    await add_to_cart.click()

    # Step 4: Verify that the cart contains an item
    cart_link = async_page.locator("#nav-cart")

    await expect(cart_link).to_contain_text(
        "1",
        timeout=15000
    )

    print("Product added to cart successfully.")

    # Step 5: Open the cart
    await cart_link.evaluate(
        "(element) => element.scrollIntoView({block: 'center'})"
    )

    await expect(cart_link).to_be_visible(timeout=10000)
    await cart_link.click()

    # Step 6: Verify the cart page
    await async_page.wait_for_load_state("domcontentloaded")
    await async_page.wait_for_timeout(2000)

    print("Cart URL:", async_page.url)

    assert "/gp/cart/" in async_page.url, (
    f"Expected the cart page, but got: {async_page.url}"
    )

    print("Cart page opened successfully.")