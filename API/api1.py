
import asyncio
from playwright.async_api import async_playwright
import pytest

@pytest.mark.asyncio
async def test_slow_network():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Slow down API requests by 3 seconds
        async def slowapi(route):
            print("API Request:", route.request.url)
            await asyncio.sleep(3)
            await route.continue_()

        await page.route("**/api/**", slowapi)

        await page.goto("https://demowebshop.tricentis.com/")

        await page.wait_for_timeout(5000)

        await browser.close()
