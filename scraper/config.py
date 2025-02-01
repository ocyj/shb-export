# scraper/config.py
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.LOGIN_URL = os.getenv('LOGIN_URL', 'https://example.com/login')
        self.USERNAME = os.getenv('SHB_USERNAME')
        self.TIMEOUT = int(os.getenv('TIMEOUT', 30))  # Default to 30 if not set

    @classmethod
    def load_from_env(cls):
        load_dotenv()
        config = cls()

        # Validate required environment variables
        missing_vars = []
        if not config.USERNAME:
            missing_vars.append('USERNAME')
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

        return config