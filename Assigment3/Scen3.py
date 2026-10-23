#Sceanorio 3
import asyncio
import re
import pytest
from playwright.async_api import Page, async_playwright, expect


async def search_with_dynamic_autocomplete(
    page: Page, partial_text: str, target_suggestion_keyword: str
) -> dict:
    
    search_input = page.locator("#twotabsearchtextbox")
    await expect(search_input).to_be_visible(timeout=10000)

    await search_input.click()
    await search_input.press_sequentially(partial_text, delay=120)

    suggestions_container = page.locator(".autocomplete-results-container, .left-pane-results-container")
    suggestion_items = page.locator("div.s-suggestion, div.s-suggestion-container")

    has_suggestions = False
    try:
        await expect(suggestions_container).to_be_visible(timeout=4000)
        await expect(suggestion_items.first).to_be_visible(timeout=2000)
        has_suggestions = True
    except AssertionError:
        has_suggestions = False

    outcome_data = {
        "partial_text": partial_text,
        "autocomplete_present": has_suggestions,
        "selected_method": None,
        "final_query": None,
        "navigated_url": None,
    }

    if has_suggestions:
        outcome_data["selected_method"] = "autocomplete_suggestion"
        print("[Status] Autocomplete suggestions appeared.")
        matching_suggestion = suggestion_items.filter(
            has_text=re.compile(re.escape(target_suggestion_keyword), re.IGNORECASE)
        ).first

        if await matching_suggestion.count() == 0:
            print(f"[Warning] '{target_suggestion_keyword}' not found in suggestions. Falling back to first item.")
            matching_suggestion = suggestion_items.first

        chosen_text = (await matching_suggestion.inner_text()).strip()
        print(f"[Action] Selecting suggestion: '{chosen_text}'")

        async with page.expect_navigation(wait_until="domcontentloaded"):
            await matching_suggestion.click()

        outcome_data["final_query"] = chosen_text

    else:
        outcome_data["selected_method"] = "search_submit_button"
        print("[Status] Autocomplete absent or suppressed. Falling back to Search button.")

        search_button = page.locator("#nav-search-submit-button")
        await expect(search_button).to_be_visible()

        async with page.expect_navigation(wait_until="domcontentloaded"):
            await search_button.click()

        outcome_data["final_query"] = partial_text

    results_container = page.locator("div[data-component-type='s-search-result']")
    await expect(results_container.first).to_be_visible(timeout=10000)

    outcome_data["navigated_url"] = page.url
    print(f"[Verification] Successfully navigated. Current URL: {page.url}")

    return outcome_data


@pytest.mark.asyncio
async def test_search_with_dynamic_autocomplete(async_page):
    await async_page.goto("https://www.amazon.in", wait_until="domcontentloaded")
    result_summary = await search_with_dynamic_autocomplete(
        page=async_page,
        partial_text="keych",
        target_suggestion_keyword="keychron k2",
    )
    assert result_summary["navigated_url"] is not None
    assert "amazon.in" in result_summary["navigated_url"]
    await async_page.wait_for_timeout(3000)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        page = await context.new_page()

        print("Opening Amazon India...")
        await page.goto("https://www.amazon.in", wait_until="domcontentloaded")

        result_summary = await search_with_dynamic_autocomplete(
            page=page,
            partial_text="keych",
            target_suggestion_keyword="keychron k2",
        )

        print("\n--- Execution Report ---")
        for key, value in result_summary.items():
            print(f"{key}: {value}")

        await browser.close()


        if __name__ == "__main__":
         asyncio.run(main())