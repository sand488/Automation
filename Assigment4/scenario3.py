import pytest

from playwright.async_api import (
    expect,
    TimeoutError as PlaywrightTimeoutError,
)

from helpers import SEARCH_BOX, SEARCH_BUTTON, RESULT_CARD


# Scenario 3: Autocomplete Suggestions or Search Fallback

@pytest.mark.asyncio
@pytest.mark.amazon
async def test_autosuggest_or_fallback_to_search(
    amazon_page,
    product_keyword,
):
    page = amazon_page

    # Step 1: Open Amazon India
    await page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded",
        timeout=60000,
    )

    # Step 2: Locate the search box
    search = page.locator(SEARCH_BOX)

    await expect(search).to_be_visible(timeout=20000)

    # Step 3: Enter part of the product keyword
    partial = product_keyword[:max(3, len(product_keyword) // 2)]
    await search.fill(partial)

    # Step 4: Check autocomplete suggestions
    suggestions = page.locator(
        'div[role="row"], div.s-suggestion, div[role="option"]'
    )

    try:
        await suggestions.first.wait_for(
            state="visible",
            timeout=2500,
        )

        texts = [
            text.strip()
            for text in await suggestions.all_inner_texts()
            if text.strip()
        ]

        print("Autocomplete suggestions:", texts[:8])

        matching = None

        for index in range(await suggestions.count()):
            item = suggestions.nth(index)
            text = " ".join((await item.inner_text()).split())

            if product_keyword.casefold() in text.casefold():
                matching = item
                break

        # Step 5: Select a matching suggestion or use Search
        if matching:
            await matching.click()
            print("Matching suggestion selected.")

        else:
            print("No matching suggestion. Clicking Search.")
            await page.locator(SEARCH_BUTTON).click()

    except PlaywrightTimeoutError:
        print("Autocomplete unavailable. Clicking Search.")
        await page.locator(SEARCH_BUTTON).click()

    # Step 6: Verify that search results are displayed
    await page.wait_for_load_state(
        "domcontentloaded",
        timeout=30000,
    )

    await expect(
        page.locator(RESULT_CARD).first
    ).to_be_visible(timeout=20000)

    print("Search results loaded successfully.")
    print("Final URL:", page.url)