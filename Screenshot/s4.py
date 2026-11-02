
import pytest
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_sc():

    path_full = "D:/AI/Python_playwright/screenshots/page1.png"
    path_logo = "D:/AI/Python_playwright/screenshots/logo.png"

    # Create screenshot folder
    Path("D:/AI/Python_playwright/screenshots").mkdir(
        parents=True, exist_ok=True
    )

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        await page.set_viewport_size({
            "width": 1280,
            "height": 800
        })

        await page.goto(
            "https://demowebshop.tricentis.com/",
            wait_until="domcontentloaded"
        )

        # Take logo screenshot
        await page.locator(".header-logo").screenshot(
            path=path_logo
        )

        # Take full webpage screenshot
        await page.screenshot(
            path=path_full,
            full_page=True
        )

        await browser.close()

    # Crop and resize screenshot using Pillow
    with Image.open(path_full) as image:

        width, height = image.size

        crop_box = (0, 0, width, 250)

        crop_img = image.crop(crop_box)

        target_size = (800, 150)

        resize_img = crop_img.resize(
            target_size,
            Image.Resampling.LANCZOS
        )

        resize_img.save(
            "D:/AI/Python_playwright/screenshots/re-size.png"
        )
