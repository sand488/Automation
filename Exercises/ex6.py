def test_locators_get_by_role(page):
    page.goto("https://demowebshop.tricentis.com/")
    page.getbyrole("link", name="Log in").click()
    page.getbyrole("textbox", name="Email").fill("abc@gmail.com")
    page.getbyrole("textbox", name="Password").fill("123456")
    page.getbyrole("button", name="Log in").click()
