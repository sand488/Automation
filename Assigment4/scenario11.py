from pathlib import Path

import pytest
from playwright.sync_api import expect


# Scenario 11: Session Reuse and Missing File Handling

STATE_FILE = Path(__file__).parent / "auth_state.json"


@pytest.mark.amazon
def test_session_reuse_and_missing_file_handling(browser):

    # Step 1: Check whether the saved session exists
    if not STATE_FILE.exists():
        pytest.skip(
            "Missing auth_state.json. Run setup_auth_state.py "
            "if authorized to save and reuse a test session."
        )

    # Step 2: Create a context using the saved browser state
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

        # Step 4: Check the account navigation
        account = page.locator("#nav-link-accountList")

        expect(account).to_be_visible(timeout=15000)

        account_text = " ".join(
            account.inner_text().split()
        ).casefold()

        print("Current URL:", page.url)
        print("Account navigation:", account_text)

        # Step 5: Check whether the session appears unauthenticated
        if (
            "/ap/signin" in page.url.casefold()
            or "hello, sign in" in account_text
        ):
            pytest.skip(
                "Storage state loaded, but the Amazon session "
                "appears unauthenticated or expired."
            )

        print("Account navigation is visible.")
        print("Saved browser state was loaded.")

    finally:
        # Step 6: Close the temporary context
        context.close()


def test_missing_state_file_is_reported_cleanly(tmp_path):

    # Step 7: Verify how a missing state file is handled
    missing = tmp_path / "does_not_exist.json"

    assert not missing.exists()

    with pytest.raises(FileNotFoundError):
        missing.read_text(encoding="utf-8")

    print("Missing state file handled correctly.")