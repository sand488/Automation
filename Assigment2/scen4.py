import re
from playwright.sync_api import expect

# Transfer Funds & Verify Transaction

def test_refund(page):

    # Step 1: Login
    page.goto("https://parabank.parasoft.com/parabank/index.htm")

    page.locator("//input[@name='username']").fill("Sandy1239000")
    page.locator("//input[@name='password']").fill("123456785676")

    page.locator("//input[@value='Log In']").click()

    # Step 2: Navigate to Accounts Overview
    page.locator("//a[text()='Accounts Overview']").click()

    # Wait for account numbers to load
    account_locator = page.locator(
        "#accountTable tbody tr td:first-child a"
    )

    expect(account_locator.first).to_be_visible(timeout=15000)

    # Retrieve account numbers
    all_accounts = account_locator.all_text_contents()

    if len(all_accounts) < 2:
        raise AssertionError(
            f"Expected at least 2 accounts, but found: {all_accounts}"
        )

    account1 = all_accounts[0].strip()
    account2 = all_accounts[1].strip()

    print("Account number 1:", account1)
    print("Account number 2:", account2)

    # Step 3: Transfer Funds
    page.locator("//a[text()='Transfer Funds']").click()

    page.locator("#amount").fill("50")

    # Select accounts dynamically
    page.locator("#fromAccountId").select_option(account1)
    page.locator("#toAccountId").select_option(account2)

    # Click Transfer
    page.locator("//input[@value='Transfer']").click()

    # Step 4: Verify transfer result
    page.locator("#showResult").wait_for(
        state="visible",
        timeout=15000
    )

    title_text = page.locator("#showResult h1").inner_text()
    amount_text = page.locator("#amountResult").inner_text().strip()
    from_acc = page.locator("#fromAccountIdResult").inner_text().strip()
    to_acc = page.locator("#toAccountIdResult").inner_text().strip()

    print("Status:", title_text)
    print("Amount Transferred:", amount_text)
    print("From Account:", from_acc)
    print("To Account:", to_acc)

    # Verify the transfer details
    expect(page.locator("#amountResult")).to_have_text("$50.00")
    expect(page.locator("#fromAccountIdResult")).to_have_text(account1)
    expect(page.locator("#toAccountIdResult")).to_have_text(account2)

    print("Transfer confirmation verified successfully!")

    # Step 5: Navigate to Accounts Overview
    page.locator("//a[text()='Accounts Overview']").click()

    # Step 6: Open the source account
    page.locator(f"//a[normalize-space()='{account1}']").click()

    # Verify that the source account details are displayed
    expect(
        page.get_by_text("Account Details", exact=True)
    ).to_be_visible()

    print("Source account details opened:", account1)

    # Step 7: Navigate back to Accounts Overview
    page.locator("//a[text()='Accounts Overview']").click()

    # Step 8: Open the destination account
    page.locator(f"//a[normalize-space()='{account2}']").click()

    # Verify that the destination account details are displayed
    expect(
        page.get_by_text("Account Details", exact=True)
    ).to_be_visible()

    print("Destination account details opened:", account2)

    print("Scenario completed successfully!")