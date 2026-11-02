
import pytest
from pathlib import Path
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_sc():

    path_full = "D:/AI/Python_playwright/screenshots/page1.png"
    path_logo = "D:/AI/Python_playwright/screenshots/logo.png"

    # Create screenshot directory
    Path("D:/AI/Python_playwright/screenshots").mkdir(
        parents=True, exist_ok=True
    )

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        await page.set_viewport_size({
            "width": 1280,
            "height": 800
        })

        await page.goto(
            "https://demowebshop.tricentis.com/",
            wait_until="domcontentloaded"
        )

        # Capture only the website logo
        await page.locator(".header-logo").screenshot(
            path=path_logo
        )

        # Capture the complete webpage
        await page.screenshot(
            path=path_full,
            full_page=True
        )

        await browser.close()
