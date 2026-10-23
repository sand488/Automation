import pytest
from playwright.sync_api import expect


# Scenario 3: Open New Account & Verify Account

def test_open_new_account(page):

    # Step 1: Open ParaBank
    page.goto(
        "https://parabank.parasoft.com/parabank/index.htm",
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("\nOpened ParaBank successfully.")

    # Step 2: Login
    page.locator("//input[@name='username']").fill("Sandy123")

    page.locator("//input[@name='password']").fill("123456785676")

    page.locator("//input[@value='Log In']").click()

    # Step 3: Verify successful login
    open_account_link = page.get_by_role(
        "link",
        name="Open New Account",
        exact=True
    )

    try:
        expect(open_account_link).to_be_visible(timeout=15000)

    except AssertionError:
        page_text = page.locator("body").inner_text()

        pytest.fail(
            "Login failed or Open New Account link is unavailable.\n"
            f"Current URL: {page.url}\n"
            f"Page content:\n{page_text[:1000]}"
        )

    print("Login successful!")

    # Step 4: Navigate to Open New Account
    open_account_link.click()

    # Step 5: Select account type (Savings)
    page.locator("#type").select_option("1")

    # Step 6: Wait for the existing account dropdown
    from_account = page.locator("#fromAccountId")

    expect(from_account).to_be_visible(timeout=15000)

    # Wait until an existing account is available
    expect(from_account.locator("option")).not_to_have_count(
        0,
        timeout=15000
    )

    # Select the first available account
    account_options = from_account.locator("option")

    account_count = account_options.count()

    selected_account = None

    for i in range(account_count):
        option_value = account_options.nth(i).get_attribute("value")

        if option_value:
            selected_account = option_value
            break

    assert selected_account is not None, (
        "No existing account is available to open a new account."
    )

    from_account.select_option(selected_account)

    print("Existing account selected:", selected_account)

    # Step 7: Open the new account
    page.locator(
        "//input[@value='Open New Account']"
    ).click()

    # Step 8: Verify account creation
    expect(
        page.get_by_role(
            "heading",
            name="Account Opened!",
            exact=True
        )
    ).to_be_visible(timeout=15000)

    print("New account opened successfully!")

    # Step 9: Capture the generated account number
    account_number = page.locator("#newAccountId")

    expect(account_number).to_be_visible(timeout=15000)

    new_account_number = account_number.inner_text().strip()

    assert new_account_number, (
        "A new account number was not generated."
    )

    print("New Account Number:", new_account_number)

    # Step 10: Navigate to Accounts Overview
    page.get_by_role(
        "link",
        name="Accounts Overview",
        exact=True
    ).click()

    # Step 11: Verify Accounts Overview
    expect(
        page.get_by_role(
            "heading",
            name="Accounts Overview",
            exact=True
        )
    ).to_be_visible(timeout=15000)

    print("Accounts Overview opened successfully.")

    # Step 12: Verify the new account appears in the account list
    new_account_link = page.locator(
        f"#accountTable a:text-is('{new_account_number}')"
    )

    expect(new_account_link).to_be_visible(timeout=15000)

    print(
        f"PASS: New account {new_account_number} "
        "is displayed in Accounts Overview."
    )