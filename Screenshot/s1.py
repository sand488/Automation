
import pytest
from pathlib import Path
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_sc():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        await page.goto(
            "https://demowebshop.tricentis.com/",
            wait_until="domcontentloaded"
        )

        # Create screenshot folder if it does not exist
        screenshot_folder = Path("D:/AI/Python_playwright/screenshots")
        screenshot_folder.mkdir(parents=True, exist_ok=True)

        await page.screenshot(
            path=str(screenshot_folder / "page.png"),
            full_page=True,
            mask=[
                page.locator(".timestamp"),
                page.locator(".dynamic-banner")
            ],
            mask_color="#FF00FF"
        )

        await browser.close()
