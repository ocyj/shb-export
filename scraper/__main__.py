import asyncio
from .browser import init_browser
from .login import LoginHandler
from .config import Config


async def main():
    config = Config.load_from_env()
    playwright, browser, page = await init_browser(headless=False)
    login_handler = LoginHandler(config, page)

    try:
        await login_handler.run()
        pass

    finally:
        await browser.close()
        await playwright.stop()


if __name__ == "__main__":
    asyncio.run(main())
