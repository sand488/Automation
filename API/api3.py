
import pytest
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_slow_network():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        try:
            page = await browser.new_page()

            response = await page.goto(
                "https://demowebshop.tricentis.com/",
                wait_until="load"
            )

            assert response is not None, "No response received"
            assert response.status < 400, (
                f"HTTP error: {response.status}"
            )

            # Wait for the browser to collect performance metrics
            await page.wait_for_timeout(1000)

            metrics = await page.evaluate("""() => {
                const timing =
                    performance.getEntriesByType('navigation')[0];

                if (!timing) {
                    return null;
                }

                return {
                    domContentLoaded:
                        timing.domContentLoadedEventEnd -
                        timing.startTime,

                    loadEvent:
                        timing.loadEventEnd -
                        timing.startTime,

                    responseTime:
                        timing.responseEnd -
                        timing.requestStart,

                    resourceCount:
                        performance.getEntriesByType('resource').length
                };
            }""")

            assert metrics is not None, (
                "Navigation timing data unavailable"
            )

            print("HTTP status:", response.status)
            print("Performance metrics:", metrics)

            assert metrics["domContentLoaded"] < 3000, (
                "DOM content loaded exceeded 2 seconds"
            )

        finally:
            await browser.close()
