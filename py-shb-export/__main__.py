import sys
import asyncio
import json
from .account_data import create_account_data_from_response
from .browser import init_browser
from .login import LoginHandler
from .config import Config
from .js_handler import JsHandler


async def main():

    if "--container" in sys.argv:
        print("Running in container mode.")
        import segno
        
        qr = segno.make("Hi there!")
        with open('/dev/tty', 'w') as tty_dev:
            qr.terminal(tty_dev, compact=True)
        
        exit()
    else:
        print("Running in non-container mode.")
        exit()

    config = Config.load_from_env()
    playwright, browser, page = await init_browser(headless=False)

    js_handler = JsHandler(page)
    login_handler = LoginHandler(config, page)

    try:
        await js_handler.load_js()
        await login_handler.login()

        txn_data = []
        
        for account in config.ACCOUNTS:
            response = await js_handler.req_transactions(account)
            txn_data.append(create_account_data_from_response(response))
        
        json.dumps(txn_data, indent=2)
        await login_handler.logout()
        pass

    finally:
        await page.close()
        await browser.close()
        await playwright.stop()


if __name__ == "__main__":
    asyncio.run(main())
