# README

Export your transactions from Handelsbanken's web page. Requires Python 3.13.

## Set up for development

1. `git clone ... && cd ...`
1. `python -m venv venv`
1. `.\venv\Scripts\Activate.ps1` | `source venv/bin/activate`
1. `pip install pip-tools`
1. `pip-sync`
1. `playwright install`
1. Copy `example.env` to `.env`.
1. Edit `.env` as required.
1. Run with `python -m py_shb_export > shb_transactions.json`.

## Docker

Easiest way to run the exporter.

### Build

1. `version=$(python -c "import py_shb_export; print(py_shb_export.__version__)")`
1. `docker build -t shb-export:$version .`

### Run
1. Make sure a valid `.env`-file exists in working directory.
1. `docker run --rm --env-file .env -a stdout -a stderr shb-export > shb_transactions.json`

## Disclaimer

This project is provided for educational and informational purposes only. The author makes no warranties, express or implied, regarding the accuracy, reliability, or suitability of the software for any particular purpose. Use of this software is at your own risk.

**Important:**

- The author is not affiliated with or endorsed by any financial institution.
- It is the responsibility of the user to ensure that any use of this software complies with the terms of service of their bank and all applicable laws and regulations.
- The software is provided "as is," and the author will not be liable for any direct, indirect, incidental, or consequential damages arising from its use.
- Nothing in this repository should be construed as legal advice. If you have any questions regarding the legality of using this software, please consult with a qualified legal professional.

By using this software, you acknowledge that you have read this disclaimer and agree to assume full responsibility for its use.
