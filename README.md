# CP Concierge

Automates purchasing train tickets on the Portuguese Railways (CP) website using Playwright.

This small automation script drives a Chromium browser to search for a trip on https://cp.pt, fill passenger details and proceed to the payment step. It's intended as a convenience script for repeatable bookings — use responsibly and make sure it complies with CP's terms of service.

## Features

- Search for a trip by origin, destination, date and time
- Support for multiple passengers (IDs, names, Rail Green Pass info)
- Fills passenger and contact information and proceeds to payment

## Station Codes

- Lisboa Oriente: 94-31039
- Lisboa Santa Apolonia: 94-30007
- Coimbra-B: 94-36004
- Aveiro: 94-3800
- Santarem: 94-38000
- Sete Rios: 94-66076
- Tunes: 94-78006
- Evora: 94-83006
- Guarda: 94-49007
- Mortagua: 94-46243

## Requirements

- Python 3.8+
- The packages listed in `requirements.txt` (Playwright, python-dotenv, etc.)
- Playwright browsers installed (see install steps)

## Installation

1. Create a virtual environment (recommended):

```pwsh
python -m venv .venv
. .venv\Scripts\Activate.ps1
```

2. Install dependencies:

```pwsh
python -m pip install -r requirements.txt
```

3. Install Playwright browsers:

```pwsh
python -m playwright install
```

4. Create exe

```pwsh
$env:PLAYWRIGHT_BROWSERS_PATH="0"
playwright install chromium
pyinstaller -F main.py
```

5. Run Docker
```pwsh
docker run --rm -it -e DRY_RUN=$DRY_RUN -e LOGIN=$LOGIN -e SLOW_MO=$SLOW_MO -e HEADLESS=$HEADLESS -e EMAIL=$EMAIL -e PASSWORD=$PASSWORD -e ORIGIN=$ORIGIN -e DESTINATION=$DESTINATION -e DEPARTURE_DATE=$DEPARTURE_DATE -e DEPARTURE_TIME=$DEPARTURE_TIME -e IDS=$ID -e NAMES=$NAMES -e RAIL_GREEN_PASSES=$RAIL_GREEN_PASSES my-image
```

## Configuration (.env)

Create a `.env` file in the project root with the following variables (example values shown):

```
EMAIL=you@example.com
PASSWORD=your_account_password
NR_PASSENGERS=1
ORIGIN=Lisbon
DESTINATION=Porto
DEPARTURE_DATE=2025-12-01
DEPARTURE_TIME=09:00
IDS=00000000
NAMES=First Last
RAIL_GREEN_PASSES=GREENPASSID
SLOW_MO=50
HEADLESS=False
```

Notes on variables:
- `EMAIL` and `PASSWORD`: account credentials used by the script to log in when needed.
- `NR_PASSENGERS`: integer number of passengers.
- `IDS`, `NAMES`, `RAIL_GREEN_PASSES`: comma-separated lists matching the number of passengers (order matters).
- `SLOW_MO`: Playwright slow motion in milliseconds (useful to watch actions). Set to `0` for no delay.
- `HEADLESS`: set to `True` to run without opening a browser window.

## Usage

After installing dependencies and creating `.env`, run:

```pwsh
# From project root
python main.py
```

The script will open a Chromium browser, perform the trip search, fill passenger data and proceed to the payment step. The script stops at the payment screen — you will need to complete payment manually.

## Important notes & safety

- Do NOT commit your `.env` file or credentials to source control.
- Automating actions on a third-party site can violate terms of service. Confirm that your usage is allowed by CP before running this script.
- Use responsibly to avoid accidental duplicate bookings or charges.

## Troubleshooting

- If Playwright fails to start, ensure you installed browsers with `python -m playwright install`.
- If selectors stop working, the CP site likely changed its UI — you'll need to update selector usage in `main.py`.

## Development

- Code is contained in `main.py`. It's synchronous Playwright code (`playwright.sync_api`).
- To change behavior, edit `main.py` and re-run.

## License

This repository has no license specified. Add a `LICENSE` file if you plan to publish or share this project.
