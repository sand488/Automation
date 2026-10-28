
import json
import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_slow_network():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        async def modify_req(route):
            req = route.request
            print("Request URL:", req.url)

            # Get existing headers
            headers = await req.all_headers()

            # Add custom header
            headers["x-test-client"] = "playwright-Async"

            # Modify JSON POST payload
            if req.method == "POST" and req.post_data:
                try:
                    payload = json.loads(req.post_data)

                    if isinstance(payload, dict):
                        print("Original payload:", payload)

                        if "quantity" in payload:
                            payload["quantity"] = 5
                            updated_payload = json.dumps(payload)

                            print("Updated payload:", updated_payload)

                            await route.continue_(
                                headers=headers,
                                post_data=updated_payload
                            )
                            return

                except json.JSONDecodeError:
                    print("Request body is not JSON")

            # Continue all other requests
            await route.continue_(headers=headers)

        await page.route("**/api/**", modify_req)

        await page.goto("https://demowebshop.tricentis.com/")
        await page.wait_for_timeout(5000)

        await browser.close()
