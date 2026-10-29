
import pytest
from pathlib import Path
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_trace():

    # STEP 1: Create tracing folder
    trace_dir = Path("D:/AI/Python_playwright/tracing")
    trace_dir.mkdir(parents=True, exist_ok=True)

    trace_file = trace_dir / "trace1.zip"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # STEP 2: Start tracing
        await context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        try:
            page = await context.new_page()

            # STEP 3: Open registration page
            await page.goto(
                "https://parabank.parasoft.com/parabank/register.htm"
            )

            username = "1213random123"
            password = "abc@123"

            # STEP 4: Fill registration form
            await page.locator(
                'input[name="customer.firstName"]'
            ).fill("abc")

            await page.locator(
                'input[name="customer.lastName"]'
            ).fill("a")

            await page.locator(
                'input[name="customer.address.street"]'
            ).fill("10 Test Street")

            await page.locator(
                'input[name="customer.address.city"]'
            ).fill("Bengaluru")

            await page.locator(
                'input[name="customer.address.state"]'
            ).fill("Karnataka")

            await page.locator(
                'input[name="customer.address.zipCode"]'
            ).fill("560001")

            await page.locator(
                'input[name="customer.phoneNumber"]'
            ).fill("9876543210")

            await page.locator(
                'input[name="customer.ssn"]'
            ).fill("123456789")

            await page.locator(
                'input[name="customer.username"]'
            ).fill(username)

            await page.locator(
                'input[name="customer.password"]'
            ).fill(password)

            await page.locator(
                'input[name="repeatedPassword"]'
            ).fill(password)

            # STEP 5: Submit registration
            await page.locator(
                'input[value="Register"]'
            ).click()

            # STEP 6: Validate registration result
            await expect(
                page.locator("#rightPanel")
            ).to_contain_text("Welcome", timeout=10000)

            print(f"[PASS] Registration successful: {username}")

        except Exception as e:
            print(f"[FAIL] Error: {e}")
            raise

        finally:
            # STEP 7: Save trace
            try:
                await context.tracing.stop(
                    path=str(trace_file)
                )
                print(f"[TRACE SAVED] {trace_file}")
            finally:
                await context.close()
                await browser.close()


# Run:
# python -m pytest test_trace.py -v -s

# Open trace:
# python -m playwright show-trace "D:/AI/Python_playwright/tracing/trace1.zip"
