from dotenv import load_dotenv
import os

load_dotenv()

def test_navigate(page):
    page.goto(os.getenv("BASE_URL"))
    assert page.title() == "Demo Web Shop"

