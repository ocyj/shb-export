# scraper/config.py
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.PNR = os.getenv('SHB_PERSONNUMMER')

    @classmethod
    def load_from_env(cls):
        load_dotenv()
        config = cls()

        # Validate required environment variables
        missing_vars = []
        if not config.PNR:
            missing_vars.append('SHB_PERSONNUMMER')
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

        return config