import io
import asyncio
import segno
from PIL import Image
from pyzbar.pyzbar import decode
from aiofiles import open as aio_open
from .config import Config
from .constants import Constants, Selectors

QR_SELECTOR = '[data-test-id="QrCode__image"]'
PNR_SELECTOR = '[data-test-id="PersonalIdTypeInput__input"]'
MBID_LOGON_SELECTOR = '[data-test-id="MBIDStartStage__loginButton"]'


def display_qr_in_terminal(data: str):
    qr = segno.make(data)
    qr.terminal(compact=True)

# async def load_js_script(file_path: str) -> str:
#     async with aio_open(file_path, 'r', encoding='utf-8') as file:
#         return await file.read()

class LoginHandler:
    def __init__(self, config: Config, page):
        self.config = config
        self.page = page

    async def _handle_element_update(self):
        print('QR code update detected!')
        qr_element = await self.page.query_selector(QR_SELECTOR)
        if qr_element:
            print('QR element found. Taking screenshot...')
            qr_screenshot = await qr_element.screenshot()
            from PIL import Image
            image = Image.open(io.BytesIO(qr_screenshot))
            decoded_objects = decode(image)
            if decoded_objects:
                for obj in decoded_objects:
                    qr_data = obj.data.decode("utf-8")
                    print(f'Decoded QR Code Data: {qr_data}')
                    print("\033[2J\033[H", end='')
                    display_qr_in_terminal(qr_data)
            else:
                print('No QR Data found in the screenshot.')
        else:
            print('QR element not found.')

    async def run(self):

        await self.page.expose_function("notifyPython", lambda: asyncio.create_task(self._handle_element_update()))
        await self.page.goto(Constants.SHB_LOGON_URL)

        async with aio_open("./scraper/inject_observers.js", 'r', encoding='utf-8') as file:
            js_observers_str = await file.read()

        # js_observer_start = await load_js_script('./scraper/qr_observer_start.js')
        # js_observer_stop = await load_js_script('./scraper/qr_observer_stop.js')
        await self.page.evaluate(js_observers_str)
        print("MutationObserver injected.")
        print("Navigated to the login page.")
        
        pnr_input = await self.page.wait_for_selector(PNR_SELECTOR)
        await pnr_input.fill(self.config.PNR)

        # Wait for the button to be visible/clickable and click it.
        login_button = await self.page.wait_for_selector(MBID_LOGON_SELECTOR)
        await login_button.click()
        
        await self.page.wait_for_selector(QR_SELECTOR)
        await self.page.evaluate("window.initQrObserver()")
        print("QR selector found.")

        await self._handle_element_update()

        await self.page.wait_for_selector(Selectors.LOGOUT_BUTTON)

        # You can then implement your keep-alive logic or further steps
        # For example:
        # try:
        #     while True:
        #         await asyncio.sleep(1)
        # except asyncio.CancelledError:
        #     await self.page.evaluate(js_observer_stop)
        #     print("Observer stopped.")
