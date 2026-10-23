import pytest
import pytest_asyncio
from playwright.async_api import async_playwright


# Fixture 1: Launch a browser and provide an asynchronous page
@pytest_asyncio.fixture
async def amazon_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(
            viewport={"width": 1440, "height": 900}
        )

        page = await context.new_page()

        yield page

        await context.close()
        await browser.close()


# Fixture 2: Provide the product keyword for Scenario 1
@pytest.fixture
def product_keyword():
    return "Logitech"