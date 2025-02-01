import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from .config import Config

def main():
    cfg = Config.load_from_env()
    print(f"config {cfg.USERNAME}")
    # try:
    #     username = os.getenv("USERNAME")
    #     password = os.getenv("PASSWORD")

    #     print(f'username/pw: {username} {password}')
    #     with sync_playwright() as p:
    #         browser = p.chromium.launch(headless=headless)  # Set to False for debugging
    #         page = browser.new_page()
    #         page.goto("https://example.com")
    #         print(page.title())
    #         browser.close()
    # except Exception as e:
    #     print(f"An error occurred: {e}")

if __name__ == "__main__":
    
    main()
