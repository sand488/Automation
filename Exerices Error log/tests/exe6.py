# test_api_monitoring

import pytest
from playwright.async_api import async_playwright
from logger_config import logger

@pytest.mark.asyncio
async def test_api_monitoring():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        async def handle_request(req):
            if "/api/" in req.url.lower():
                print("\n--- API REQUEST ---")
                print("URL:", req.url)
                print("Method:", req.method)
                print("Headers:", await req.all_headers())
                print("Payload:", req.post_data)

        page.on("request", handle_request)

        async def handle_response(res):
            if "/api/" in res.url.lower():
                print("\n--- API RESPONSE ---")
                print("URL:", res.url)
                print("Status:", res.status)

                content_type = res.headers.get(
                    "content-type", ""
                )

                if "application/json" in content_type:
                    try:
                        print("JSON:", await res.json())
                    except Exception as error:
                        print("Could not read JSON:", error)

        page.on("response", handle_response)

        try:
            await page.goto(
                "https://parabank.parasoft.com/parabank/index.htm"
            )

            await page.get_by_text(
                "Register", exact=True
            ).click()

        finally:
            await browser.close()