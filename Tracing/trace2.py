
import json
import subprocess
from pathlib import Path

import pytest
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_lighthouse_audit():

    # STEP 1: Open website using Playwright
    url = "https://demowebshop.tricentis.com/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        try:
            page = await browser.new_page()
            await page.goto(url, wait_until="load", timeout=60000)

            print("Website opened:", await page.title())

        finally:
            await browser.close()

    # STEP 2: Define report location
    project_dir = Path(__file__).resolve().parent
    report_path = project_dir / "lighthouse-report.json"

    # STEP 3: Run Lighthouse audit
    try:
        result = subprocess.run(
            [
                "npx.cmd",
                "--yes",
                "lighthouse",
                url,
                "--chrome-flags=--headless",
                "--output=json",
                f"--output-path={report_path}",
            ],
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=180,
            shell=False,
        )

    except subprocess.TimeoutExpired:
        pytest.fail("Lighthouse audit timed out after 180 seconds")

    # STEP 4: Check Lighthouse execution
    if result.stdout:
        print("Lighthouse output:", result.stdout)

    if result.returncode != 0:
        pytest.fail(
            f"Lighthouse audit failed.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    # STEP 5: Read Lighthouse JSON report
    with report_path.open(encoding="utf-8") as file:
        report = json.load(file)

    # STEP 6: Print Lighthouse scores
    for name in (
        "performance",
        "accessibility",
        "best-practices",
        "seo",
    ):
        score = report["categories"][name]["score"]

        if score is not None:
            print(f"{name}: {score * 100:.0f}/100")
        else:
            print(f"{name}: Score unavailable")

    print("JSON report saved to:", report_path)


# Run:

