# README

Export your transactions from Handelsbanken's web page.

## Set up for development

1. `git clone ... && cd ...`
1. `python -m venv venv`
1. `.\venv\Scripts\Activate.ps1` | `source venv/bin/activate`
1. `pip install pip-tools`
1. `pip-sync`
1. `playwright install`
1. Copy `example.env` to `.env`
1. Edit `.env` as required
1. Run with `python scraper.py`

### Build and run with docker

1. `docker build -t -t shb_scrape .`
1. `docker run --rm --env-file .env scraper.py`
