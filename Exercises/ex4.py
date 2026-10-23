from playwright.sync_api import sync_playwright, expect

def test_application(browser):
    #with sync_playwright() as p:
        #browser = browser.launch(headless=False)
        end_user_context = browser.new_context()
        end_user_page = end_user_context.new_page()
        end_user_page.goto("https://www.google.com/")
        # expect(act).to_have_title(exp)
        expect(end_user_page).to_have_title("Google")

#      #admin_user
        admin_context =browser.new_context()
        admin_page = admin_context.new_page()
        admin_page.goto("https://www.google.com/")
        expect(admin_page).to_have_title("Google")
