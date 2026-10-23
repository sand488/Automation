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

    await async_page.wait_for_timeout(3000)

    print("\n========== HOME PAGE DETAILS ==========")
    print("Home title:", await async_page.title())
    print("Home URL:", async_page.url)

    # Step 2: Search for women's jeans
    search_box = async_page.locator("#twotabsearchtextbox")
    await expect(search_box).to_be_visible(timeout=20000)

    await search_box.fill("Jeans for women")
    await async_page.locator("#nav-search-submit-button").click()

    # Wait for the search results page
    await async_page.wait_for_load_state(
        "domcontentloaded",
        timeout=30000
    )

    await async_page.wait_for_timeout(3000)

    print("\n========== SEARCH PAGE DETAILS ==========")
    print("Search title:", await async_page.title())
    print("Search URL:", async_page.url)

    # Save a screenshot for debugging
    await async_page.screenshot(
        path="amazon_debug.png",
        full_page=True
    )

    # Save the current page HTML for inspection
    html_content = await async_page.content()

    with open("amazon_debug.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("Saved screenshot: amazon_debug.png")
    print("Saved HTML: amazon_debug.html")

    # Step 3: Locate product containers
    results = async_page.locator(
        "div[data-component-type='s-search-result']"
    )

    product_count = await results.count()

    print("\n========== PRODUCT CONTAINER DIAGNOSTICS ==========")
    print("Product container count:", product_count)

    if product_count == 0:
        pytest.fail(
            "No Amazon product containers were found. "
            "Check amazon_debug.png and amazon_debug.html. "
            "The page may not have loaded the expected search results."
        )

    await expect(results.first).to_be_visible(timeout=30000)

    # Step 4: Diagnose different product title selectors
    selector_1 = async_page.locator(
        "div[data-component-type='s-search-result'] h2 a"
    )

    selector_2 = async_page.locator(
        "div[data-component-type='s-search-result'] a:has(h2)"
    )

    selector_3 = async_page.locator(
        "div[data-component-type='s-search-result'] h2"
    )

    selector_4 = async_page.locator(
        "a:has(h2)"
    )

    print("\n========== SELECTOR DIAGNOSTICS ==========")
    print("Selector 1 — product container h2 a:",
          await selector_1.count())

    print("Selector 2 — product container a:has(h2):",
          await selector_2.count())

    print("Selector 3 — product container h2:",
          await selector_3.count())

    print("Selector 4 — page-wide a:has(h2):",
          await selector_4.count())

    # Print the first product container's HTML
    first_product_html = await results.first.evaluate(
        "(element) => element.outerHTML"
    )

    print("\n========== FIRST PRODUCT CONTAINER HTML ==========")
    print(first_product_html[:5000])

    # Print the first few links containing an h2
    heading_link_count = await selector_4.count()

    print("\n========== LINKS CONTAINING H2 ==========")

    for index in range(min(heading_link_count, 5)):
        link = selector_4.nth(index)

        print(f"\nLink {index + 1}:")
        print("Text:", (await link.inner_text()).strip())
        print("Href:", await link.get_attribute("href"))

    # Step 5: Select a product title locator
    # Prefer links inside Amazon's product containers.
    if await selector_1.count() > 0:
        product_links = selector_1
        print("\nUsing selector 1: product container h2 a")

    elif await selector_2.count() > 0:
        product_links = selector_2
        print("\nUsing selector 2: product container a:has(h2)")

    elif await selector_4.count() > 0:
        product_links = selector_4
        print("\nUsing selector 4: page-wide a:has(h2)")

    else:
        pytest.fail(
            "Product containers were found, but none of the tested "
            "selectors found a link containing an h2. "
            "Inspect amazon_debug.html and the printed HTML to identify "
            "the actual product title link structure."
        )

    # Print the final selected locator count
    link_count = await product_links.count()

    print("\n========== SELECTED PRODUCT LINKS ==========")
    print("Product title link count:", link_count)

    if link_count < 2:
        pytest.fail(
            f"Expected at least 2 product title links, but found "
            f"{link_count}. Check the diagnostic output and HTML."
        )

    # Step 6: Select the second product title link
    product = product_links.nth(1)

    await expect(product).to_be_visible(timeout=20000)

    product_name = (await product.inner_text()).strip()
    product_href = await product.get_attribute("href")
    product_target = await product.get_attribute("target")

    print("\n========== SELECTED PRODUCT ==========")
    print("Selected product:", product_name)
    print("Selected product href:", product_href)
    print("Selected product target:", product_target)

    if not product_href:
        pytest.fail("The selected product link has no href attribute.")

    # Step 7: Click product and handle a new tab if applicable
    if product_target == "_blank":
        async with async_page.expect_popup() as popup_info:
            await product.click()

        product_page = await popup_info.value
    else:
        await product.click()
        product_page = async_page

    await product_page.wait_for_load_state(
        "domcontentloaded",
        timeout=30000
    )

    await product_page.wait_for_timeout(2000)

    print("\n========== PRODUCT PAGE DETAILS ==========")
    print("Product page URL:", product_page.url)

    # Step 8: Verify that the product page opened
    product_title = product_page.locator("span#productTitle")

    await expect(product_title).to_be_visible(timeout=20000)

    actual_product_title = (
        await product_title.inner_text()
    ).strip()

    assert actual_product_title, "Product title is empty."

    print("Opened product title:", actual_product_title)

    print("\nScenario 1 completed successfully.")