# test_browser_logging

import pytest
from playwright.async_api import async_playwright
from logger_config import logger

@pytest.mark.asyncio
async def test_browser_logging():
    logger.info("========== TEST EXECUTION STARTED ==========")
    browser = None

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            # Capture browser console messages
            page.on(
                "console",
                lambda msg: logger.error(
                    "BROWSER CONSOLE [%s]: %s",
                    msg.type.upper(),
                    msg.text
                ) if msg.type == "error" else None
            )

            # Capture JavaScript errors
            page.on(
                "pageerror",
                lambda error: logger.error(
                    "JAVASCRIPT ERROR: %s", error
                )
            )

            # Capture failed requests
            page.on(
                "requestfailed",
                lambda request: logger.error(
                    "REQUEST FAILED: %s | Error: %s",
                    request.url,
                    request.failure
                )
            )

            # Capture HTTP error responses
            page.on(
                "response",
                lambda response: logger.warning(
                    "HTTP ERROR: %s | Status: %s",
                    response.url,
                    response.status
                ) if response.status >= 400 else None
            )

            logger.info("Opening Demo Web Shop")

            await page.goto(
                "https://demowebshop.tricentis.com/",
                wait_until="domcontentloaded"
            )

            logger.info("Page title: %s", await page.title())

            search_box = page.get_by_role(
                "textbox", name="Search store"
            )

            await search_box.fill("book")
            await page.get_by_role(
                "button", name="Search"
            ).click()

            await page.locator(".product-item").first.wait_for(
                state="visible"
            )

            logger.info("Search results are visible")
            logger.info("TEST RESULT: PASSED")

    except Exception:
        logger.exception("TEST RESULT: FAILED")
        raise

    finally:
        if browser is not None:
            await browser.close()

        logger.info("========== TEST EXECUTION FINISHED ==========")
