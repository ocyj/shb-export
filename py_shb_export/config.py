# scraper/config.py
import os
import sys
from datetime import date
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.PNR = os.getenv('SHB_PERSONNUMMER')
        self.ACCOUNTS = os.getenv('SHB_ACCOUNTS').split(';')
        self.IN_CONTAINER = (os.getenv('SHB_DOCKER', False)) == 'TRUE'
        self.FROM_DATE = None

    @classmethod
    def load(cls):
        load_dotenv()
        config = cls()

        # Validate required environment variables
        missing_vars = []
        if not config.PNR:
            missing_vars.append('SHB_PERSONNUMMER')
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")
    
        args = sys.argv[1:]

        if not args:
            return config

        if len(args) != 2 or args[0] != "--from":
            raise ValueError(
                "Usage: py_shb_export [--from YYYY-MM-DD]\n"
                f"Got arguments: {args!r}"
            )

        date_str = args[1]
        try:
            from_date = date.fromisoformat(date_str)
            config.FROM_DATE = from_date.isoformat()
        except ValueError:
            raise ValueError(
                f"Invalid date {date_str!r}. Expected format YYYY-MM-DD (e.g. 2025-09-01)."
            )

        return config