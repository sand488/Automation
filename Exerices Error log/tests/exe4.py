# test_block_resources

import pytest
from playwright.async_api import async_playwright
from logger_config import logger

@pytest.mark.asyncio
async def test_block_resources():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        async def intercept(route):
            request = route.request
            url = request.url.lower()
            resource_type = request.resource_type

            if resource_type in ["image", "font"]:
                print("BLOCKED RESOURCE:", url)
                await route.abort()

            elif "analytics" in url:
                print("BLOCKED ANALYTICS:", url)
                await route.abort()

            else:
                await route.continue_()

        await page.route("**/*", intercept)

        try:
            await page.goto(
                "https://parabank.parasoft.com/parabank/index.htm"
            )

            await page.get_by_text(
                "Register", exact=True
            ).click()

            await page.wait_for_load_state("domcontentloaded")

        finally:
            await browser.close()
