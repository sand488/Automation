import re
import pytest
from playwright.async_api import expect


# Scenario 2: Select and Interact with a Product Card

@pytest.mark.asyncio
async def test_select_and_interact_card(async_page):

    # Step 1: Open Amazon India
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    # Step 2: Search for a Logitech wireless mouse
    search_box = async_page.locator("#twotabsearchtextbox")
    await search_box.fill("Logitech wireless mouse")
    await search_box.press("Enter")

    # Step 3: Find the product card containing Logitech in its title
    product_cards = async_page.locator(
        "div[data-component-type='s-search-result']"
    )

    matching_card = product_cards.filter(
        has=async_page.locator(
            "h2",
            has_text=re.compile("Logitech", re.IGNORECASE)
        )
    ).first

    await expect(matching_card).to_be_visible(timeout=20000)

    # Step 4: Verify the product title
    product_title = matching_card.locator("h2").first
    title = (await product_title.inner_text()).strip()

    print("Selected Product:", title)

    # Step 5: Click Add to Cart if available
    add_to_cart = matching_card.locator(
        "button[name='submit.addToCart'], "
        "input[name='submit.addToCart'], "
        "button:has-text('Add to cart')"
    ).first

    if await add_to_cart.is_visible():
        await add_to_cart.click()
        print("Add to Cart clicked successfully.")

    else:
        # Step 6: Otherwise, open the product page
        product_link = matching_card.locator("a:has(h2)").first

        if await product_link.get_attribute("target") == "_blank":
            async with async_page.expect_popup() as popup:
                await product_link.click()

            product_page = await popup.value
        else:
            await product_link.click()
            product_page = async_page

        # Step 7: Verify the product page
        visible_title = product_page.locator("span#productTitle")

        await expect(visible_title).to_be_visible(timeout=20000)

        actual_title = (await visible_title.inner_text()).strip()

        print("Opened Product:", actual_title)

        assert "Logitech" in actual_title.lower() or \
            "logitech" in actual_title.lower(), (
                f"Unexpected product title: {actual_title}"
            )

    print("Scenario 2 completed successfully.")
