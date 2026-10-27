#Exercise 1
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


#Exercise 2
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


#Exercise 3
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


#Exercise 4
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

#Exercise 5

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


#Exercise 6
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