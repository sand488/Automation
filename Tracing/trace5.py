
import pytest
from playwright.async_api import async_playwright
from pytest_check import check


@pytest.mark.asyncio
async def test_sanity_dom_check():

    url = "https://parabank.parasoft.com/parabank/register.htm"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        try:
            page = await browser.new_page()
            await page.goto(url, wait_until="domcontentloaded")

            # STEP 1: Check page title
            title = await page.title()
            print("Page title:", title)

            check.is_true(
                bool(title.strip()),
                "Page title is missing"
            )

            # STEP 2: Check images missing alt attributes
            images_without_alt = page.locator("img:not([alt])")
            count = await images_without_alt.count()

            meaningful_missing_alt = 0

            print("Images missing alt attribute:", count)

            for i in range(count):
                image = images_without_alt.nth(i)

                width = await image.evaluate(
                    "(img) => img.naturalWidth"
                )
                height = await image.evaluate(
                    "(img) => img.naturalHeight"
                )
                src = await image.get_attribute("src")

                print(
                    f"Image {i + 1}: {src}, "
                    f"dimensions: {width}x{height}"
                )

                # Ignore tiny 1x1 layout images
                if width > 1 or height > 1:
                    meaningful_missing_alt += 1
                    print("Meaningful image missing alt:", src)

            check.equal(
                meaningful_missing_alt,
                0,
                f"{meaningful_missing_alt} meaningful images "
                "lack alt attributes"
            )

            # STEP 3: Check main landmark
            main_count = await page.locator(
                "main, [role='main']"
            ).count()

            print("Main landmarks found:", main_count)

            if main_count == 1:
                print("PASS: Main landmark found")
            else:
                print(
                    f"WARNING: Expected 1 main landmark, "
                    f"found {main_count}"
                )

            print("DOM sanity checks completed")

        finally:
            await browser.close()
