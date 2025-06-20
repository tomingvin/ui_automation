# This file contains the reusable login and logout example functions with responsive logic.

from playwright.sync_api import Page, expect
from config.users import USERS
from config.urls import URLS

def login(page: Page, user_key: str, url_key: str):

    # --- Get configuration ---
    user_config = USERS.get(user_key)
    if not user_config:
        raise ValueError(f"Invalid user key provided: '{user_key}'")

    url = URLS.get(url_key)
    if not url:
        raise ValueError(f"Invalid URL key provided: '{url_key}'")
    

    # Responsive Login Steps
    viewport_size = page.viewport_size
    
    # Mobile view (width <= 991px)
    if viewport_size and viewport_size['width'] <= 991:
        page.get_by_role("button", name="Menu").click()
        page.get_by_role("button", name="Log ind").click()
        page.wait_for_load_state("networkidle")

    
        page.locator("#menuButton").click()
    
        page.get_by_role("link", name="Test login").click()

    # Desktop view (width > 991px)
    else:
        page.get_by_role("button", name="Log ind").click()
        page.wait_for_load_state("networkidle")
        page.get_by_role("link", name="Test login").click()

    # Common login steps for both mobile and desktop

    page.wait_for_load_state("networkidle")

    page.locator("#somelocator").click()
    page.locator("#somelocator").type(user_config["username"])

    page.locator("#somelocator").click()
    page.locator("#somelocator").type(user_config["password"])
    page.wait_for_load_state("networkidle")

    login_button = page.get_by_role("button", name="Log on").or_(page.get_by_role("button", name="Log på"))
    login_button.click()

def logout(page: Page):

    viewport_size = page.viewport_size
    
    # Mobile view (width <= 991px)
    if viewport_size and viewport_size['width'] <= 991:
        page.wait_for_load_state("networkidle")
        print("--- DEBUG: Printing HTML before clicking mobile menu for logout ---")
        print(page.content())
        page.get_by_role("button", name="Menu").click()
        page.get_by_role("button", name="Log ud").click()
    # Desktop view (width > 991px)
    else:
        page.get_by_role("button", name="Log ud").click(timeout=10000)

