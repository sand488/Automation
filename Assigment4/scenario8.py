import pytest
from playwright.async_api import expect


# Scenario 8: Mock Multi-Step Form Persists Values

@pytest.mark.asyncio
@pytest.mark.mock
async def test_mock_multistep_form_persists_values(amazon_page):

    page = amazon_page

    # Step 1: Create the mock multi-step form
    await page.set_content("""
    <!doctype html>
    <html>
    <body>
        <h1>Trainer Mock Checkout</h1>

        <section id="step1">
            <label for="recipient">Test recipient</label>
            <input id="recipient" name="recipient">
            <button id="next" type="button">Continue</button>
        </section>

        <section id="step2" hidden>
            <label for="delivery">Delivery note</label>
            <input id="delivery" name="delivery">
            <button id="back" type="button">Back</button>
        </section>

        <script>
            document.querySelector("#next").onclick = () => {
                document.querySelector("#step1").hidden = true;
                document.querySelector("#step2").hidden = false;
            };

            document.querySelector("#back").onclick = () => {
                document.querySelector("#step2").hidden = true;
                document.querySelector("#step1").hidden = false;
            };
        </script>
    </body>
    </html>
    """)

    # Step 2: Enter the recipient
    recipient = page.get_by_label("Test recipient")

    await recipient.fill("Demo User")

    # Step 3: Navigate to the second step
    await page.get_by_role(
        "button",
        name="Continue"
    ).click()

    delivery = page.get_by_label("Delivery note")

    await expect(delivery).to_be_visible()

    # Step 4: Enter the delivery note
    await delivery.fill("Leave at demo desk")

    # Step 5: Navigate back to the first step
    await page.get_by_role(
        "button",
        name="Back"
    ).click()

    # Step 6: Verify the recipient value was preserved
    await expect(
        page.get_by_label("Test recipient")
    ).to_have_value("Demo User")

    # Step 7: Return to the second step
    await page.get_by_role(
        "button",
        name="Continue"
    ).click()

    # Step 8: Verify the delivery note was preserved
    await expect(
        page.get_by_label("Delivery note")
    ).to_have_value("Leave at demo desk")

    print("PASS: Both form values persisted across navigation.")
    print("Scenario 8 completed successfully.")
