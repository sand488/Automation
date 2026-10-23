import re
import pytest

from playwright.async_api import Page, expect


# Shared Amazon locators
SEARCH_BOX = "#twotabsearchtextbox"
SEARCH_BUTTON = "#nav-search-submit-button"
RESULT_CARD = "div[data-component-type='s-search-result']"


# Amazon product-title selectors
TITLE_SELECTORS = (
    '[data-cy="title-recipe-title"]',
    ".a-size-base-plus.a-color-base.a-text-normal",
    ".a-size-medium.a-color-base.a-text-normal",
    "h2 a span",
    "h2 span",
    "h2",
)


# Internal helper: Collect visible title candidates from a card
async def _visible_title_candidates(card):

    candidates = []

    for selector in TITLE_SELECTORS:
        elements = card.locator(selector)

        for index in range(await elements.count()):
            element = elements.nth(index)

            if not await element.is_visible():
                continue

            text = " ".join((await element.inner_text()).split())

            if text and text not in candidates:
                candidates.append(text)

    return candidates


# Helper 1: Search for a product on Amazon
async def search_amazon(
    page: Page,
    product_keyword: str,
) -> None:

    await page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded",
        timeout=60000,
    )

    search_box = page.locator(SEARCH_BOX)

    await expect(search_box).to_be_visible(timeout=20000)

    await search_box.fill(product_keyword)
    await search_box.press("Enter")

    await page.wait_for_load_state(
        "domcontentloaded",
        timeout=30000,
    )

    print(f"Searching for: {product_keyword}")


# Helper 2: Find a matching product card
async def find_product_card(
    page: Page,
    product_keyword: str,
):

    product_cards = page.locator(RESULT_CARD)

    await expect(
        product_cards.first
    ).to_be_visible(timeout=20000)

    expected_terms = set(
        re.findall(r"[a-z0-9]+", product_keyword.casefold())
    )

    inspected_titles = []

    for index in range(await product_cards.count()):

        card = product_cards.nth(index)

        # Read visible title elements
        titles = await _visible_title_candidates(card)
        inspected_titles.extend(titles)

        # Include visible card text and image descriptions
        metadata = titles + [
            await card.inner_text()
        ]

        images = card.locator("img")

        for image_index in range(await images.count()):
            alt = await images.nth(
                image_index
            ).get_attribute("alt")

            if alt:
                metadata.append(alt)

        # Include link labels where available
        links = card.locator("a")

        for link_index in range(await links.count()):
            link = links.nth(link_index)

            for attribute in ("aria-label", "title"):
                value = await link.get_attribute(attribute)

                if value:
                    metadata.append(value)

        searchable_text = " ".join(metadata).casefold()

        actual_terms = set(
            re.findall(r"[a-z0-9]+", searchable_text)
        )

        phrase_match = (
            " ".join(product_keyword.split()).casefold()
            in searchable_text
        )

        all_terms_match = (
            bool(expected_terms)
            and expected_terms.issubset(actual_terms)
        )

        if phrase_match or all_terms_match:
            print(f"Matching product card found: {index}")
            print("Visible title candidates:", titles[:5])

            return card

    pytest.fail(
        f"No product card matched '{product_keyword}'.\n"
        "Visible title candidates inspected:\n"
        + "\n".join(
            f"- {title}"
            for title in list(dict.fromkeys(inspected_titles))[:20]
        )
    )


# Helper 3: Extract the product title from a card
async def card_title(
    card,
    expected_title: str | None = None,
) -> str:

    candidates = await _visible_title_candidates(card)

    if not candidates:
        pytest.fail(
            "No visible product-title element was found in the card."
        )

    # When an expected title is supplied, select a visible candidate
    # that contains all expected title terms.
    if expected_title:

        expected_terms = set(
            re.findall(r"[a-z0-9]+", expected_title.casefold())
        )

        matching_titles = [
            title
            for title in candidates
            if expected_terms.issubset(
                set(re.findall(r"[a-z0-9]+", title.casefold()))
            )
        ]

        if matching_titles:
            expected_length = len(
                " ".join(expected_title.split())
            )

            return min(
                matching_titles,
                key=lambda title: abs(
                    len(title) - expected_length
                ),
            )

        pytest.fail(
            f"No visible title matched '{expected_title}'.\n"
            f"Visible candidates: {candidates!r}"
        )

    # Without an expected title, prefer the most descriptive candidate
    return max(candidates, key=len)


# Helper 4: Extract the visible product price
async def visible_price(card):

    price_elements = card.locator(
        "span.a-price:not(.a-text-price)"
    )

    for index in range(await price_elements.count()):

        price_element = price_elements.nth(index)

        if not await price_element.is_visible():
            continue

        price_text = price_element.locator(".a-offscreen")

        if await price_text.count() == 0:
            continue

        text = await price_text.first.text_content()

        if text and text.strip():
            return text.strip()

    # A price may not be available for every card
    return None


# Helper 5: Open the product and return its title
async def open_card_product(
    page: Page,
    card,
) -> str:

    product_link = card.locator("a:has(h2)").first

    await expect(
        product_link
    ).to_be_visible(timeout=10000)

    target = await product_link.get_attribute("target")
    product_page = page

    # Handle products opening in a new tab
    if target == "_blank":

        async with page.expect_popup() as popup_info:
            await product_link.click()

        product_page = await popup_info.value

    else:
        await product_link.click()

    try:
        await product_page.wait_for_load_state(
            "domcontentloaded",
            timeout=30000,
        )

        title_locator = product_page.locator(
            "span#productTitle"
        )

        await expect(
            title_locator
        ).to_be_visible(timeout=20000)

        title = (
            await title_locator.inner_text()
        ).strip()

        print(f"Opened product: {title}")

        return title

    finally:
        # Close only a newly opened product tab
        if product_page is not page:
            await product_page.close()