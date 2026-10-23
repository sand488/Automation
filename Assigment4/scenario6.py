import pytest
from playwright.async_api import expect

from helpers import (
    search_amazon,
    find_product_card,
    card_title,
)


# Scenario 6: Verify Product Context Survives Navigation

@pytest.mark.asyncio
@pytest.mark.amazon
async def test_product_context_survives_navigation(
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

    # Step 3: Capture the product link
    product_link = card.locator("a:has(h2)").first

    await expect(product_link).to_be_visible(timeout=10000)

    selected_href = await product_link.get_attribute("href")

    assert selected_href, (
        "Selected product does not have a destination link."
    )

    # Step 4: Open the product in the same tab
    # Amazon may set target="_blank"; remove it to test back navigation.
    await product_link.evaluate(
        "(element) => element.removeAttribute('target')"
    )

    await product_link.click()

    # Step 5: Verify the product details page
    product_title = page.locator("span#productTitle")

    await expect(product_title).to_be_visible(timeout=20000)

    detail_title = " ".join(
        (await product_title.inner_text()).split()
    )

    print("Product details title:", detail_title)

    assert (
        selected_title.casefold() in detail_title.casefold()
        or detail_title.casefold() in selected_title.casefold()
    ), (
        f"Product titles differ. "
        f"Search result={selected_title!r}; "
        f"Details page={detail_title!r}"
    )

    # Step 6: Navigate back to search results
    await page.go_back(wait_until="domcontentloaded")

    # Step 7: Verify the search context is preserved
    search_box = page.locator("#twotabsearchtextbox")

    await expect(search_box).to_be_visible(timeout=15000)

    restored_keyword = await search_box.input_value()

    assert product_keyword.casefold() in restored_keyword.casefold(), (
        f"Search keyword was not preserved. "
        f"Expected={product_keyword!r}; "
        f"Actual={restored_keyword!r}"
    )

    print("Back navigation successful.")
    print("Restored search keyword:", restored_keyword)
    print("Scenario 6 completed successfully.")