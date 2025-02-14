class Constants:
    SHB_LOGON_URL = "https://secure.handelsbanken.se/logon/se/priv/sv/mbidqr/"

class Selectors:
    SHB_LOGIN_BUTTON = '[data-test-id="shb-sepu-header__login-button"]'
    SHB_LOGOUT_BUTTON = '[data-testid="ApplicationHeaderLogOutButton"]'
    SHB_MBID_LOGON = '[data-test-id="MBIDStartStage__loginButton"]'
    SHB_PNR_INPUT = '[data-test-id="PersonalIdTypeInput__input"]'
    SHB_QR_DISPLAY = '[data-test-id="QrCode__image"]'