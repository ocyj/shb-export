import re
import importlib.resources

from playwright.async_api import Page

import py_shb_export
from .constants import Selectors as s, Constants as c


def _load_resource(resource_name, placeholders: dict = None):
    file_content = importlib.resources.read_text(py_shb_export, 'res/js', resource_name, encoding='utf-8')
    if(placeholders):
        return _replace_placeholders(file_content, placeholders)
    return file_content


def _replace_placeholders(template: str, mapping: dict) -> str:
    """
    Replace placeholders in the template string with values from mapping.
    
    Placeholders are of the form '____PH_key____', where 'key' corresponds to 
    a key in the mapping dict.
    
    Args:
        template: The input string containing placeholders.
        mapping: A dict where each key corresponds to the unique identifier in the placeholder.
    
    Returns:
        A new string with all placeholders replaced by their corresponding values.
    
    Raises:
        ValueError: If there are any placeholders that were not replaced.
    """
    # The regex captures any characters between '____PH_' and '____'
    pattern = r"____PH_(.*?)____"
    
    def repl(match):
        key = match.group(1)
        # Replace the placeholder with the value from the dict if it exists,
        # otherwise leave it unchanged.
        return str(mapping.get(key, match.group(0)))
    
    result = re.sub(pattern, repl, template)
    
    # Check for any remaining placeholders
    unresolved = re.search(pattern, result)
    if unresolved:
        raise ValueError(f"Unresolved placeholder found: {unresolved.group(0)}")
    
    return result


# TODO: split me into multiple (three?) sub classes
class JsHandler:
    def __init__(self, page: Page):
        self.page = page

        self.JS_RES_REQ_ACCTS_FILE = 'req_account_transactions.js'
        self.JS_RES_REQ_FN = '____get_transactions'
        self.JS_RES_REQ_ACCTS_MAPPINGS = {
            'reqfn': self.JS_RES_REQ_FN,
            'requrl': c.SHB_TXN_REQ_URL
            }
        
        self.JS_INJ_QR_OBS_FILE = 'inject_qr_observer.js'
        self.JS_INJ_QR_OBS_CALLBACK = '____notify_qr_change'
        self.JS_INJ_QR_OBS_INIT_FN = '____init_qr_obs'
        self.JS_INJ_QR_OBS_MAPPINGS = {
            'qrsel': s.SHB_QR_DISPLAY,
            'pycallback': self.JS_INJ_QR_OBS_CALLBACK,
            'initqrobs' : self.JS_INJ_QR_OBS_INIT_FN
        }

        self.JS_COOKIE_MODAL_FILE = 'close_cookie_modal.js'
        self.JS_COOKIE_MODAL_OBS_INIT_FN = '____init_cookie_mod_obs'
        self.JS_COOKIE_MODAL_MAPPINGS = {
            'cookiemodal': s.SHB_COOKIE_MODAL,
            'cookiedecline': s.SHB_COOKIE_MODAL_DECLINE_BUTTON,
            'initcookieobsfn': self.JS_COOKIE_MODAL_OBS_INIT_FN
         #   'cookieclose': self.JS_COOKIE_MODAL_CHECK_FN
        }


    async def load_js(self):
        js_req =  _load_resource(self.JS_RES_REQ_ACCTS_FILE, self.JS_RES_REQ_ACCTS_MAPPINGS)
        js_qr_obs = _load_resource(self.JS_INJ_QR_OBS_FILE, self.JS_INJ_QR_OBS_MAPPINGS)
        js_cookie_modal = _load_resource(self.JS_COOKIE_MODAL_FILE, self.JS_COOKIE_MODAL_MAPPINGS)

        await self.page.add_init_script(script=js_req)
        await self.page.add_init_script(script=js_qr_obs)
        await self.page.add_init_script(script=js_cookie_modal)


    async def req_transactions(self, account_number: str):
        arg = {'account': f'{account_number}~INLÅ~N'}
        return await self.page.evaluate(f'(arg) => window.{self.JS_RES_REQ_FN}(arg)', arg)


    async def init_qr_observer(self):
        await self.page.evaluate(f"window.{self.JS_INJ_QR_OBS_INIT_FN}()")


    async def init_cookie_modal_observer(self):
         await self.page.evaluate(f"window.{self.JS_COOKIE_MODAL_OBS_INIT_FN}()")


# if __name__ == '__main__':
#     # Example usage:
#     template_js = """
#     console.log("Value of x: ____PH_x____");
#     console.log("Value of y: ____PH_y____");
#     console.log("Value of z: ____PH_z____");
#     """

#     mapping = {
#     "x": "Hello, World!",
#     "y": "42",
#     "z": "NO wAY"
#     }

#     try:
#         result = _replace_placeholders(template_js, mapping)
#         print(result)
#     except ValueError as e:
#         print("Error:", e)