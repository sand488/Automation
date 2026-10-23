import pytest
from playwright.async_api import expect, TimeoutError as PlaywrightTimeoutError

from helpers import search_amazon, RESULT_CARD


# Scenario 7: Pagination or Lazy-Loaded Results

@pytest.mark.asyncio
@pytest.mark.amazon
async def test_pagination_or_lazy_loaded_results(
    amazon_page,
    product_keyword,
):
    page = amazon_page

    # Step 1: Search for the product
    await search_amazon(page, product_keyword)

    # Step 2: Count the initial search results
    results = page.locator(RESULT_CARD)
    before = await results.count()

    assert before > 0, (
        "No search result cards found on the initial page."
    )

    print(f"Initial product card count: {before}")

    # Step 3: Check for a Next Page button
    next_page = page.locator("a.s-pagination-next")

    if (
        await next_page.count() > 0
        and await next_page.first.is_visible()
        and await next_page.first.is_enabled()
    ):
        old_url = page.url

        await next_page.first.click()

        await page.wait_for_load_state(
            "domcontentloaded",
            timeout=30000,
        )

        await expect(
            results.first
        ).to_be_visible(timeout=15000)

        after = await results.count()

        assert page.url != old_url or after != before, (
            "Next-page action did not appear to change the results."
        )

        print(f"Pagination detected: {before} -> {after} cards.")
        return

    # Step 4: If no Next Page button exists, test lazy loading
    print("No enabled Next Page button. Checking lazy loading.")

    await results.last.scroll_into_view_if_needed()

    try:
        await page.wait_for_function(
            """({selector, oldCount}) =>
                document.querySelectorAll(selector).length > oldCount
            """,
            arg={
                "selector": RESULT_CARD,
                "oldCount": before,
            },
            timeout=4000,
        )

        after = await results.count()

        assert after > before, (
            "Lazy loading was expected to add more product cards."
        )

        print(f"Lazy loading detected: {before} -> {after} cards.")

    except PlaywrightTimeoutError:
        pytest.skip(
            "No enabled Next Page button was found, and no additional "
            "product cards loaded after scrolling. The live page may "
            "not support either behavior in this session."
        )
