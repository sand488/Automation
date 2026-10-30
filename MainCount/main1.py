
import pytest
from pathlib import Path
from playwright.async_api import async_playwright
from pytest_check import check


# Set True to enforce accessibility validation.
# Set False to report defects without failing pytest.
STRICT_ACCESSIBILITY = False


@pytest.mark.asyncio
async def test_sanity_dom_check():

    url = "https://demowebshop.tricentis.com/"

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        try:

            page = await browser.new_page(
                viewport={"width": 1366, "height": 768}
            )

            await page.goto(
                url,
                wait_until="domcontentloaded"
            )

            print("\n========== DOM SANITY CHECK ==========")

            # 1. Page Title Validation

            title = await page.title()

            print("\nPage Title:", title)

            check.is_true(
                bool(title.strip()),
                "Page title is missing"
            )

            # 2. Image ALT Validation

            missing_alt = await page.locator(
                "img:not([alt])"
            ).count()

            print("\nImages Missing ALT:", missing_alt)

            check.equal(
                missing_alt,
                0,
                f"{missing_alt} images are missing ALT attributes"
            )

            # 3. Main Landmark Validation

            main_count = await page.get_by_role("main").count()

            print("\nMain Landmark Count:", main_count)

            if main_count == 0:
                print("DEFECT: Main landmark is missing")

            # 4. Semantic Landmark Validation

            print("\n========== LANDMARK CHECK ==========")

            landmarks = {
                "Header": "header",
                "Navigation": "nav",
                "Main": "main",
                "Footer": "footer"
            }

            for name, selector in landmarks.items():

                count = await page.locator(selector).count()

                print(f"{name} count: {count}")

            # 5. Load axe-core

            print("\n========== AXE-CORE CHECK ==========")

            axe_path = (
                Path(__file__).resolve().parent
                / "node_modules"
                / "axe-core"
                / "axe.min.js"
            )

            if not axe_path.exists():

                pytest.fail(
                    "axe-core not found. Run npm install axe-core"
                )

            await page.add_script_tag(
                path=str(axe_path)
            )

            # 6. Run Accessibility Scan

            result = await page.evaluate("""
                async () => {
                    return await axe.run(document);
                }
            """)

            violations = result["violations"]

            total_affected = sum(
                len(v["nodes"]) for v in violations
            )

            print("\nTotal Violations:", len(violations))
            print("Total Affected Elements:", total_affected)

            # 7. Print Violation Details

            for violation in violations:

                print("\n-----------------------------------")

                print("Rule ID:", violation["id"])
                print("Impact:", violation["impact"])
                print("Description:", violation["description"])

                for node in violation["nodes"]:

                    print("\nAffected Element:", node["target"])
                    print("HTML:", node["html"])
                    print("Failure Details:", node["failureSummary"])

            # 8. Accessibility Summary

            print("\n========== ACCESSIBILITY SUMMARY ==========")

            print("Passed Rules:", len(result["passes"]))
            print("Failed Rules:", len(violations))
            print("Affected Elements:", total_affected)

            # 9. Screenshot Capture

            if violations or main_count != 1:

                screenshot_path = (
                    Path(__file__).resolve().parent
                    / "sanity_check.png"
                )

                await page.screenshot(
                    path=str(screenshot_path),
                    full_page=True
                )

                print("\nScreenshot saved:", screenshot_path)

            # 10. Strict Accessibility Validation
            # Main landmark is checked only ONCE.

            if STRICT_ACCESSIBILITY:

                check.equal(
                    main_count,
                    1,
                    f"Expected 1 main landmark but found {main_count}"
                )

                check.equal(
                    len(violations),
                    0,
                    f"Accessibility violations found: {len(violations)}"
                )

            # 11. Final Result

            print("\n========== FINAL TEST RESULT ==========")

            if main_count == 1 and len(violations) == 0:

                print("SITE ACCESSIBILITY STATUS: PASS")

            else:

                print("SITE ACCESSIBILITY STATUS: DEFECTS FOUND")

            print("AUDIT EXECUTION: COMPLETED")

        finally:

            await browser.close()

            print("\nBrowser closed successfully")


