from aiofiles import open as aio_open

from playwright.async_api import Page

async def load_file(filename, placeholder = None):
    async with aio_open(f'py_shb_export/{filename}', 'r', encoding='utf-8') as file:
        file_content = await file.read()
        if(placeholder):
            return file_content.replace('____PH____', placeholder)
        return file_content

class JsHandler:
    def __init__(self, page: Page):
        self.page = page

        self.REQ_ACCOUNT_TRANSACTIONS = '____req_account_transactions'
    
    async def load_js(self):
        js = await load_file(f'{self.REQ_ACCOUNT_TRANSACTIONS}.js', self.REQ_ACCOUNT_TRANSACTIONS)
        await self.page.add_init_script(script=js)
    
    async def req_transactions(self, account_number: str):
        arg = {'account': f'{account_number}~INLÅ~N'}
        return await self.page.evaluate(f'(arg) => window.{self.REQ_ACCOUNT_TRANSACTIONS}(arg)', arg)
