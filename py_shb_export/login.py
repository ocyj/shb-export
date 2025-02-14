import io
import asyncio
from PIL import Image
from pyzbar.pyzbar import decode
from aiofiles import open as aio_open
from .config import Config
from .constants import Constants, Selectors
from .terminal_writer import TerminalWriter


class LoginHandler:
    def __init__(self, config: Config, page, terminal_writer):
        self.config = config
        self.page = page
        self.tw = terminal_writer


    async def _handle_element_update(self):
        
        qr_element = await self.page.query_selector(Selectors.SHB_QR_DISPLAY)
        if qr_element:
            
            qr_screenshot = await qr_element.screenshot()
            
            image = Image.open(io.BytesIO(qr_screenshot))
            decoded_objects = decode(image)
            if decoded_objects:
                # for obj in decoded_objects:
                #     qr_data = obj.data.decode("utf-8")
                #     print(f'Decoded QR Code Data: {qr_data}')
                #     print("\033[2J\033[H", end='')
                #     display_qr_in_terminal(qr_data)
                qr_data = decoded_objects[0].data.decode("utf-8")
                self.tw.put_qr(qr_data)
            else:
                print('No QR Data found in the screenshot.')
        else:
            print('QR element not found.')


    async def login(self):

        await self.page.expose_function("notifyPython", lambda: asyncio.create_task(self._handle_element_update()))
        await self.page.goto(Constants.SHB_LOGON_URL)

        async with aio_open("./py_shb_export/inject_observers.js", 'r', encoding='utf-8') as file:
            js_observers_str = await file.read()

        # js_observer_start = await load_js_script('./scraper/qr_observer_start.js')
        # js_observer_stop = await load_js_script('./scraper/qr_observer_stop.js')
        await self.page.evaluate(js_observers_str)
        
        pnr_input = await self.page.wait_for_selector(Selectors.SHB_PNR_INPUT)
        await pnr_input.fill(self.config.PNR)

        # Wait for the button to be visible/clickable and click it.
        login_button = await self.page.wait_for_selector(Selectors.SHB_MBID_LOGON)
        await login_button.click()
        
        await self.page.wait_for_selector(Selectors.SHB_QR_DISPLAY)
        await self.page.evaluate("window.initQrObserver()")

        self.tw.clear()

        await self._handle_element_update()
        await self.page.wait_for_selector(Selectors.SHB_LOGOUT_BUTTON)
        self.tw.clear()


    async def logout(self):
        await self.page.wait_for_selector(Selectors.SHB_LOGOUT_BUTTON)
        await self.page.click(Selectors.SHB_LOGOUT_BUTTON)
        await self.page.wait_for_selector(Selectors.SHB_LOGIN_BUTTON)
