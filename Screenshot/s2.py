
import pytest
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

        await page.screenshot(
            path="D:/AI/Python_playwright/screenshots/page.png",
            full_page=True,
            mask=[
                page.locator("xpath=//input[@value='Add to cart']"),
                page.locator(".dynamic-banner")
            ],
            mask_color="#FF00FF"
        )

        await browser.close()
