# test_resource_interception

import pytest
from playwright.async_api import async_playwright
from logger_config import logger

@pytest.mark.asyncio
async def test_resource_interception():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        async def intercept(route):
            request = route.request
            url = request.url.lower()

            if request.resource_type in ("image", "font"):
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

        finally:
            await browser.close()
