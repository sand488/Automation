from pathlib import Path

import pytest
from playwright.sync_api import expect


# Scenario 10: Reuse Saved Browser Storage State

STATE_FILE = Path(__file__).parent / "auth_state.json"


@pytest.mark.amazon
def test_reuse_storage_state_if_available(browser):

    # Step 1: Check whether saved authentication state exists
    if not STATE_FILE.exists():
        pytest.skip(
            f"{STATE_FILE} not found. Create the storage state "
            "with an authorized test account if permitted."
        )

    # Step 2: Create a browser context using saved state
    context = browser.new_context(
        storage_state=str(STATE_FILE)
    )

    try:
        page = context.new_page()

        # Step 3: Open Amazon India
        page.goto(
            "https://www.amazon.in/",
            wait_until="domcontentloaded",
            timeout=60000,
        )

        print("Amazon URL:", page.url)

        # Step 4: Locate the account navigation
        account_indicator = page.locator("#nav-link-accountList")

        expect(account_indicator).to_be_visible(timeout=15000)

        account_text = " ".join(
            account_indicator.inner_text().split()
        ).casefold()

        # Step 5: Check whether the saved session appears expired
        if (
            "signin" in page.url.casefold()
            or "hello, sign in" in account_text
        ):
            pytest.skip(
                "Saved session appears unauthenticated or expired. "
                "Refresh the storage state using an authorized account."
            )

        # Step 6: Report the result
        print("Account navigation:", account_text)
        print("Saved browser state loaded successfully.")
        print(
            "Verify authenticated status separately if the account "
            "navigation does not conclusively establish it."
        )

    finally:
        # Step 7: Clean up the browser context
        context.close()
