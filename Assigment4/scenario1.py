import pytest

from helpers import (
    search_amazon,
    find_product_card,
    card_title,
    visible_price,
    open_card_product,
)


# Scenario 1: End-to-End Amazon Product Discovery

@pytest.mark.asyncio
@pytest.mark.amazon
async def test_end_to_end_product_discovery(amazon_page, product_keyword):

    # Step 1: Initialize the page
    page = amazon_page

    # Step 2: Search for the product
    await search_amazon(page, product_keyword)

    # Step 3: Find the matching product card
    card = await find_product_card(page, product_keyword)

    # Step 4: Extract product details from search results
    result_title = await card_title(card)
    price = await visible_price(card)

    # Step 5: Open the product details page
    detail_title = await open_card_product(page, card)

    # Step 6: Validate the product title
    assert (
        result_title.casefold() in detail_title.casefold()
        or detail_title.casefold() in result_title.casefold()
    ), (
        "Search-result title and detail title differ. "
        f"Result={result_title!r}; detail={detail_title!r}"
    )

    # Step 7: Print the test results
    print(
        {
            "title": detail_title,
            "price_when_visible": price,
            "url": page.url,
        }
    )

    # Step 8: Verify the Amazon URL
    assert page.url.startswith("https://www.amazon.in/"), (
        f"Unexpected page URL: {page.url}"
    )