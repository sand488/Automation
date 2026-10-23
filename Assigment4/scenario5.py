import json
from pathlib import Path

import pytest

from helpers import (
    search_amazon,
    find_product_card,
    card_title,
)


# Scenario 5: Compare UI Title with Mock API Data

MOCK_API_FILE = (
    Path(__file__).parent / "fixtures" / "product_api.json"
)


@pytest.mark.asyncio
@pytest.mark.mock
async def test_ui_title_matches_trainer_mock_api(amazon_page):

    # Step 1: Load mock API data
    if not MOCK_API_FILE.exists():
        pytest.skip(f"Mock API fixture missing: {MOCK_API_FILE}")

    data = json.loads(
        MOCK_API_FILE.read_text(encoding="utf-8")
    )

    api_title = " ".join(data["product"]["title"].split())
    api_brand = data["product"]["brand"]
    endpoint = data["source_endpoint"]

    # Step 2: Search using the brand and product title
    page = amazon_page
    search_keyword = f"{api_brand} {api_title}"

    await search_amazon(page, search_keyword)

    # Step 3: Find the corresponding product card
    card = await find_product_card(page, search_keyword)

    # Step 4: Extract the product title
    ui_title = " ".join(
        (await card_title(card)).split()
    )

    card_text = await card.inner_text()

    print("\n========== PRODUCT COMPARISON ==========")
    print("API brand:", api_brand)
    print("API title:", api_title)
    print("UI title:", ui_title)

    # Step 5: Verify the brand separately
    assert api_brand.casefold() in card_text.casefold(), (
        f"Brand mismatch. Expected {api_brand!r} in the product card."
    )

    # Step 6: Compare the actual product titles
    assert api_title.casefold() == ui_title.casefold(), (
        f"UI/API title mismatch. "
        f"Source={endpoint}; "
        f"API={api_title!r}; UI={ui_title!r}"
    )

    print("PASS: Product title and brand match the mock API.")