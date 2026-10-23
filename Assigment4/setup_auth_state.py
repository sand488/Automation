from pathlib import Path

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)


# Location where the browser session will be saved
STATE_FILE = Path(__file__).parent / "auth_state.json"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    try:
        page = context.new_page()

        # Step 1: Open Amazon India
        page.goto(
            "https://www.amazon.in/",
            wait_until="domcontentloaded",
            timeout=60000,
        )

        print("\nAmazon opened in the automation browser.")
        print("1. Log in inside this browser window.")
        print("2. Complete any OTP or verification steps.")
        print("3. Wait until you are logged in successfully.")

        input("\nAfter successful login, press Enter here...")

        # Step 2: Wait for the current navigation to settle.
        # Do not navigate to Amazon again.
        try:
            page.wait_for_load_state(
                "domcontentloaded",
                timeout=15000,
            )
        except PlaywrightTimeoutError:
            print("Page load timed out; checking the current page.")

        print("\nCurrent URL:", page.url)

        # Step 3: Check the current account navigation
        account = page.locator("#nav-link-accountList")
        account.wait_for(state="visible", timeout=15000)

        account_text = " ".join(account.inner_text().split())
        print("Account navigation:", account_text)

        # Step 4: Refuse to save if Amazon still shows sign-in
        if (
            "/ap/signin" in page.url.casefold()
            or "hello, sign in" in account_text.casefold()
        ):
            raise RuntimeError(
                "Amazon still appears to be signed out. "
                "Log in successfully in the automation browser "
                "and run this script again. Session was not saved."
            )

        # Step 5: Save the current browser state
        context.storage_state(path=str(STATE_FILE))

        print("\nBrowser storage state saved successfully.")
        print("File:", STATE_FILE)

    finally:
        context.close()
        browser.close()
