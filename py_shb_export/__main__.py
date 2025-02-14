import sys
import asyncio
import json
from .account_data import create_account_data_from_response
from .browser import init_browser
from .login import LoginHandler
from .config import Config
from .js_handler import JsHandler
from .terminal_writer import TerminalWriter


async def main():
    config = Config.load_from_env()
    headless = config.IN_CONTAINER

    playwright, browser, page = await init_browser(headless)

    tw_writer = TerminalWriter()
    js_handler = JsHandler(page)
    login_handler = LoginHandler(config, page, tw_writer, js_handler)

    try:
        await js_handler.load_js()
        await login_handler.login()

        txn_data = []
        
        for account in config.ACCOUNTS:
            response = await js_handler.req_transactions(account)
            txn_data.append(create_account_data_from_response(response))
        
        tw_writer.put_json(txn_data)

        await login_handler.logout()
        pass

    finally:
        await page.close()
        await browser.close()
        await playwright.stop()


if __name__ == "__main__":
    asyncio.run(main())
