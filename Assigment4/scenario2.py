import pytest
from playwright.async_api import expect

from helpers import (
    search_amazon,
    find_product_card,
    card_title,
)


# Scenario 2: Select Product by Visible Title

@pytest.mark.asyncio
@pytest.mark.amazon
async def test_select_product_by_visible_title(
    amazon_page,
    product_keyword
):
    # Step 1: Initialize the page
    page = amazon_page

    # Step 2: Search for the product
    await search_amazon(page, product_keyword)

    # Step 3: Find the matching product card
    card = await find_product_card(page, product_keyword)

    # Step 4: Extract and validate the product title
    title = await card_title(card)

    assert product_keyword.casefold() in title.casefold(), (
        f"Matched card title {title!r} did not contain "
        f"{product_keyword!r}"
    )

    # Step 5: Locate the product link within the matched card
    product_link = card.locator("a:has(h2)").first

    await expect(product_link).to_be_visible(timeout=10000)

    # Step 6: Verify the product link has a destination
    href = await product_link.get_attribute("href")

    assert href, (
        f"Product title link has no href: {title!r}"
    )

    print("\nProduct selected successfully:")
    print("Title:", title)
    print("Link:", href)