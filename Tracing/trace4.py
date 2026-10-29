import json
import subprocess
from pathlib import Path

import pytest
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_lighthousejson():
    url = "https://parabank.parasoft.com/parabank/register.htm"

    # Report directory and JSON file
    report_dir = Path("D:/AI/Python_playwright/light_house")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "lighthouse.json"

    username = "1213ran1dom123"
    password = "abc@123"

    # STEP 1: Register user using Python Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        try:
            page = await browser.new_page()
            await page.goto(url, wait_until="domcontentloaded")

            fields = {
                'input[name="customer.firstName"]': "abc",
                'input[name="customer.lastName"]': "a",
                'input[name="customer.address.street"]': "10 Test Street",
                'input[name="customer.address.city"]': "Bengaluru",
                'input[name="customer.address.state"]': "Karnataka",
                'input[name="customer.address.zipCode"]': "560001",
                'input[name="customer.phoneNumber"]': "9876543210",
                'input[name="customer.ssn"]': "123456789",
                'input[name="customer.username"]': username,
                'input[name="customer.password"]': password,
                'input[name="repeatedPassword"]': password,
            }

            for selector, value in fields.items():
                await page.locator(selector).fill(value)

            await page.locator('input[value="Register"]').click()
            await page.wait_for_load_state("domcontentloaded")

            print("Registration submitted")
            print("Current URL:", page.url)

        finally:
            await browser.close()

    # STEP 2: Run Lighthouse audit
    try:
        res = subprocess.run(
            [
                "npx.cmd",
                "--yes",
                "lighthouse",
                url,
                "--chrome-flags=--headless",
                "--output=json",
                f"--output-path={report_file}",
            ],
            cwd=str(report_dir),
            capture_output=True,
            text=True,
            timeout=180,
            shell=False,
        )

        if res.stdout:
            print("Lighthouse output:", res.stdout)

        if res.returncode != 0:
            print("Lighthouse error:")
            print(res.stderr)
            pytest.fail("Lighthouse audit failed")

        # STEP 3: Read Lighthouse JSON report
        with report_file.open(encoding="utf-8") as f:
            json_data = json.load(f)

        # STEP 4: Print audit scores
        for name in (
            "performance",
            "accessibility",
            "best-practices",
            "seo",
        ):
            score = json_data["categories"][name]["score"]

            if score is not None:
                print(f"{name}: {score * 100:.0f} / 100")
            else:
                print(f"{name}: Score unavailable")

        print("JSON report saved to:", report_file)

    except subprocess.TimeoutExpired:
        pytest.fail("Lighthouse timed out after 180 seconds")
        img:not([alt])