
import pytest
import shutil
from pathlib import Path
from PIL import Image, ImageChops
from playwright.async_api import async_playwright


# 1. Screenshot folder
SCREENSHOT_DIR = Path(
    r"C:\Users\User\Pictures\Screenshots"
)

BASELINE = SCREENSHOT_DIR / "baseline.png"
ACTUAL = SCREENSHOT_DIR / "actual.png"
DIFF = SCREENSHOT_DIR / "diff.png"


@pytest.mark.asyncio
async def test_visual_regression():

    # 2. Create screenshot folder
    SCREENSHOT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # 3. Launch browser
    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        try:
            page = await browser.new_page(
                viewport={"width": 1366, "height": 768},
                device_scale_factor=1
            )

            # 4. Navigate to website
            await page.goto(
                "https://www.amazon.in/",
                wait_until="domcontentloaded"
            )

            # 5. Capture actual screenshot
            await page.screenshot(
                path=str(ACTUAL),
                full_page=True
            )

            print("\nActual screenshot saved:", ACTUAL)

        finally:
            await browser.close()

    # 6. Create baseline on first execution
    if not BASELINE.exists():

        shutil.copy2(ACTUAL, BASELINE)

        print("\nBaseline screenshot created:", BASELINE)

        pytest.skip(
            "Baseline created. Review the image and run the test again."
        )

    # 7. Compare baseline and actual screenshots
    with Image.open(BASELINE) as img1, Image.open(ACTUAL) as img2:

        baseline = img1.convert("RGB")
        actual = img2.convert("RGB")

        # 8. Check image dimensions
        if baseline.size != actual.size:

            pytest.fail(
                f"Image dimensions differ: "
                f"{baseline.size} vs {actual.size}"
            )

        # 9. Find image differences
        diff = ImageChops.difference(
            baseline,
            actual
        )

        changed_pixels = sum(
            1 for pixel in diff.getdata()
            if pixel != (0, 0, 0)
        )

        total_pixels = (
            baseline.width * baseline.height
        )

        difference_ratio = (
            changed_pixels / total_pixels
        )

        # 10. Save difference screenshot
        diff.save(DIFF)

        print("\n========== VISUAL REGRESSION REPORT ==========")

        print("Changed Pixels:", changed_pixels)

        print(
            f"Difference Ratio: {difference_ratio:.4%}"
        )

        print("Diff Screenshot:", DIFF)

        # 11. Final validation
        assert difference_ratio <= 0.01, (
            f"Visual difference exceeds 1%: "
            f"{difference_ratio:.4%}"
        )

        print("\nVisual Regression Test PASSED")
