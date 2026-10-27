# test_network_monitoring

import pytest
from playwright.async_api import async_playwright
from logger_config import logger

@pytest.mark.asyncio
async def test_network_monitoring():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            record_har_path="network3_log.har"
        )
        page = await context.new_page()

        page.on(
            "console",
            lambda msg: print(
                f"[{msg.type.upper()}]: {msg.text}"
            )
        )

        page.on(
            "pageerror",
            lambda err: print(f"[PAGE ERROR] {err}")
        )

        async def handle_request(req):
            print("\n--- REQUEST ---")
            print("Method:", req.method)
            print("URL:", req.url)
            print("Payload:", req.post_data)

        page.on("request", handle_request)

        async def handle_response(res):
            content_type = res.headers.get(
                "content-type", "unknown"
            )

            print("\n--- RESPONSE ---")
            print("Status:", res.status)
            print("Content-Type:", content_type)
            print("URL:", res.url)

        page.on("response", handle_response)

        try:
            await page.goto(
                "https://parabank.parasoft.com/parabank/index.htm"
            )

            await page.get_by_text(
                "Register", exact=True
            ).click()

            await page.wait_for_load_state("domcontentloaded")

        finally:
            await context.close()
            await browser.close()
