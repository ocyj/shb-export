import io
import asyncio
from PIL import Image
from pyzbar.pyzbar import decode
from .config import Config
from .constants import Constants, Selectors
from .terminal_writer import TerminalWriter
from .js_handler import JsHandler


class LoginHandler:
    def __init__(self, config: Config, page, terminal_writer, js_handler : JsHandler):
        self.config = config
        self.page = page
        self.tw = terminal_writer
        self.js = js_handler


    async def _handle_element_update(self):
        qr_element = await self.page.query_selector(f'{Selectors.SHB_QR_DISPLAY}:visible')
        if qr_element:
            
            qr_screenshot = await qr_element.screenshot()
            
            image = Image.open(io.BytesIO(qr_screenshot))
            decoded_objects = decode(image)
            if decoded_objects:
                qr_data = decoded_objects[0].data.decode("utf-8")
                self.tw.put_qr(qr_data)
            #else:
                #print('No QR Data found in the screenshot.')
        #else:
            #print('QR element not found.')


    async def login(self):

        # TODO: Handle exposing function in JS handler class
        await self.page.expose_function(self.js.JS_INJ_QR_OBS_CALLBACK, lambda: asyncio.create_task(self._handle_element_update()))
        
        await self.page.goto(Constants.SHB_LOGON_URL)
        await self.js.init_cookie_modal_observer()


        pnr_input = await self.page.wait_for_selector(Selectors.SHB_PNR_INPUT)
        await pnr_input.fill(self.config.PNR)

        # Wait for the button to be visible/clickable and click it.
        login_button = await self.page.wait_for_selector(Selectors.SHB_MBID_LOGON)
        await login_button.click()
        
        await self.page.wait_for_selector(f'{Selectors.SHB_QR_DISPLAY}:visible')
        self.tw.clear()
        await self._handle_element_update()
        await self.js.init_qr_observer()

        await self.page.wait_for_selector(Selectors.SHB_LOGOUT_BUTTON)
        self.tw.clear()


    async def logout(self):
        await self.page.wait_for_selector(Selectors.SHB_LOGOUT_BUTTON)
        await self.page.click(Selectors.SHB_LOGOUT_BUTTON)
        await self.page.wait_for_selector(Selectors.SHB_LOGIN_BUTTON)
