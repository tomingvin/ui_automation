from playwright.sync_api import expect
from helpers.auth import login, logout
from config.urls import URLS
import os


def test_example(test_config, browser_type, browser_context_args, request):
    user_key = test_config['user']
    url_key = test_config['env']
    test_name = request.node.name

    browser = browser_type.launch(headless=False)
    context = browser.new_context(**browser_context_args)
    page = context.new_page()

    try:
        page.goto(URLS[url_key])

        login(page, user_key, url_key)

        #automation steps, use for instance Playwright's built in test generator (playwright codegen)
        # page.click('selector')
        # expect(page).to_have_text('expected text')

        logout(page)
    
    except Exception as e:
        os.makedirs("test_results", exist_ok=True)
        screenshot_path = f"test_results/{test_name}.png"
        page.screenshot(path=screenshot_path)
        print(f"Test failed — screenshot saved to {screenshot_path}")
        raise
    
    finally:
        context.close()
        browser.close()