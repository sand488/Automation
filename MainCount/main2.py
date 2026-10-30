
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

            # Navigate to website
            await page.goto(
                url,
                wait_until="domcontentloaded"
            )

            # Get page title
            title = await page.title()
            print("Page Title:", title)

            # Screenshot location
            screenshot_path = Path(
                r"C:\Users\User\Pictures\Screenshots\demo.png"
            )

            # Create folder if it doesn't exist
            screenshot_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Capture full-page screenshot
            await page.screenshot(
                path=str(screenshot_path),
                full_page=True
            )

            print("Screenshot saved successfully:", screenshot_path)

        finally:
            await browser.close()
