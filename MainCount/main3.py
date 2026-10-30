
import pytest
from pathlib import Path
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_screenshots_full_page():

    url = "https://demowebshop.tricentis.com/"

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        try:
            page = await browser.new_page()

            await page.goto(url)

            # Get page title
            title = await page.title()
            print("Page Title:", title)

            # Locate search input element
            ele = page.locator("input#small-searchterms")

            # Screenshot path
            screenshot_path = Path(
                r"C:\Users\User\Pictures\Screenshots\ele1.png"
            )

            screenshot_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Capture element screenshot
            await ele.screenshot(
                path=str(screenshot_path)
            )

            print("Element screenshot saved:", screenshot_path)

        finally:
            await browser.close()
