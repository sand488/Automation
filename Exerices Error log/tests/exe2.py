# test_har_recording

import pytest
from playwright.async_api import async_playwright
from logger_config import logger


@pytest.mark.asyncio
async def test_har_recording():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(
            record_har_path="network1_log.har"
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

        await page.goto(
            "https://parabank.parasoft.com/parabank/index.htm"
        )

        await page.get_by_text("Register", exact=True).click()

        await page.wait_for_load_state("domcontentloaded")

        # Closing the context finalizes and saves the HAR file.
        await context.close()
        await browser.close()
