import io
import asyncio
import segno
import aiofiles
from playwright.async_api import async_playwright, Page
from PIL import Image
from pyzbar.pyzbar import decode

# Define the CSS selector for the QR code element
QR_SELECTOR = '[data-test-id="QrCode__image"]'


def display_qr_in_terminal(data: str):
    """
    Generates a QR code from the provided data and displays it in the terminal.
    
    :param data: The data to encode into the QR code.
    """
    qr = segno.make(data)
    qr.terminal(compact=True, border=0)  # This prints the QR code as ASCII art in the terminal

async def load_js_script(file_path: str) -> str:
    """
    Loads a JavaScript file's content.

    :param file_path: Path to the JavaScript file.
    :return: JavaScript code as a string.
    """
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        return await file.read()

async def handle_element_update(page: Page):
    """
    Handles the QR code update by taking a screenshot and decoding it.

    :param page: Playwright Page object.
    """
    print('QR code update detected!')
    qr_element = await page.query_selector(QR_SELECTOR)

    if qr_element:
        print('QR element found. Taking screenshot...')

        # Take a screenshot of the QR element
        qr_screenshot = await qr_element.screenshot()

        # Open the image from bytes
        image = Image.open(io.BytesIO(qr_screenshot))

        # Decode the QR code using pyzbar
        decoded_objects = decode(image)
        if decoded_objects:
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                print(f'Decoded QR Code Data: {qr_data}')
                # Re-encode the data into a new QR code and display it in the terminal
                print("\033[2J\033[H", end='')
                display_qr_in_terminal(qr_data)
        else:
            print('No QR Data found in the screenshot.')
    else:
        print('QR element not found.')

async def notify_python_callback(page: Page):
    """
    Callback function exposed to JavaScript. It calls the handler for QR code updates.

    :param page: Playwright Page object.
    """
    await handle_element_update(page)

async def keep_alive():
    """
    Keeps the script running indefinitely to listen for callbacks.
    """
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass

async def monitor_class_updates():
    """
    Monitors QR code updates on a webpage using Playwright and MutationObserver.
    """
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Load JavaScript observer scripts
        js_qr_observer_start = await load_js_script('./scraper/qr_observer_start.js')
        js_qr_observer_stop = await load_js_script('./scraper/qr_observer_stop.js')

        # Expose the Python callback to JavaScript
        await page.expose_function("notifyPython", lambda: asyncio.create_task(notify_python_callback(page)))

        # Navigate to the target page
        await page.goto("https://secure.handelsbanken.se/logon/se/priv/sv/mbidqr/")
        print("Navigated to the target page.")

        # Wait for the QR selector to appear
        await page.wait_for_selector(QR_SELECTOR)
        print("QR selector found on the page.")

        # Initial handling of the QR element
        await handle_element_update(page)

        # Inject the MutationObserver JavaScript to monitor QR code changes
        await page.evaluate(js_qr_observer_start)
        print("MutationObserver injected and started.")

        # Start the keep-alive coroutine
        keep_alive_task = asyncio.create_task(keep_alive())

        # Gracefully handle shutdown
        try:
            await keep_alive_task
        except asyncio.CancelledError:
            pass
        finally:
            # Stop the MutationObserver and close the browser
            await page.evaluate(js_qr_observer_stop)
            print("MutationObserver stopped. Closing browser.")
            await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(monitor_class_updates())
    except KeyboardInterrupt:
        print("Monitoring interrupted by user.")
