
import pytest
import shutil
from pathlib import Path
from PIL import Image, ImageChops
from playwright.async_api import async_playwright


# Screenshot folder
SCREENSHOT_DIR = Path(
    r"C:\Users\User\Pictures\Screenshots"
)

BASELINE = SCREENSHOT_DIR / "baseline.png"
ACTUAL = SCREENSHOT_DIR / "actual.png"
DIFF = SCREENSHOT_DIR / "diff.png"


@pytest.mark.asyncio
async def test_visual_regression():

    # Create screenshot folder
    SCREENSHOT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        try:
            page = await browser.new_page(
                viewport={"width": 1366, "height": 768},
                device_scale_factor=1
            )

            # Open website
            await page.goto(
                "https://www.amazon.in/",
                wait_until="domcontentloaded"
            )

            # Capture actual screenshot
            await page.screenshot(
                path=str(ACTUAL),
                full_page=True
            )

            print("Actual screenshot saved:", ACTUAL)

        finally:
            await browser.close()

    # Create baseline automatically on first execution
    if not BASELINE.exists():

        shutil.copy2(ACTUAL, BASELINE)

        print("\nBaseline screenshot created:", BASELINE)
        print("Run the test again to perform visual comparison.")

        return

    # Compare baseline and actual images
    with Image.open(BASELINE) as img1, Image.open(ACTUAL) as img2:

        baseline = img1.convert("RGB")
        actual = img2.convert("RGB")

        # Check dimensions
        if baseline.size != actual.size:

            pytest.fail(
                f"Image dimensions differ: "
                f"{baseline.size} vs {actual.size}"
            )

        # Find image differences
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

        # Save difference image
        diff.save(DIFF)

        print("\n========== VISUAL REGRESSION REPORT ==========")
        print("Changed pixels:", changed_pixels)
        print(f"Difference ratio: {difference_ratio:.4%}")
        print("Diff image saved:", DIFF)

        # Final validation
        assert difference_ratio <= 0.01, (
            f"Visual difference exceeds 1%: "
            f"{difference_ratio:.4%}"
        )

        print("\nVisual regression test PASSED")
