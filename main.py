import re
import os
from dotenv import load_dotenv
from playwright.sync_api import Page, sync_playwright

import logging

level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

def login_user(page: Page, username):
    password = os.getenv("PASSWORD")

    logger.info("Logging in user")
    page.get_by_role("button", name="myCP profile").click()
    page.locator("#username").fill(username)
    page.locator("#password").fill(password)
    page.locator("#kc-login").click()



def configure_passage(page: Page, passenger):

    page.get_by_role("textbox", name="First and last name *").fill(passenger["name"])
    
    page.get_by_role("combobox", name="Identification document *").click()
    page.get_by_role("option").filter(has_text="Citizen's card").click()
    page.get_by_role("textbox", name="ID document number").fill(passenger["id"])


    page.get_by_role("combobox", name="Discount *").click()
    page.get_by_role("option").filter(has_text="Rail Green Pass").click()
    page.get_by_role("textbox", name="Additional information *").fill(passenger["rail_green_pass"])

def separate_passengers(ids, names, rail_green_passes):

    ids = ids.split(",")
    logger.debug(f"IDs: {ids}")
    names = names.split(",")
    logger.debug(f"Names: {names}")
    rail_green_passes = rail_green_passes.split(",")

    nr_passengers = len(names)

    passengers = []
    for i in range(nr_passengers):
        passenger = {
            "id": ids[i].strip(),
            "name": names[i].strip(),
            "rail_green_pass": rail_green_passes[i].strip()
        }
        passengers.append(passenger)

    return passengers, nr_passengers


def buy_ticket(page: Page, email, login):
    origin = os.getenv("ORIGIN")
    destination = os.getenv("DESTINATION")
    departure_date = os.getenv("DEPARTURE_DATE")
    departure_time = os.getenv("DEPARTURE_TIME")
    ids = os.getenv("IDS")
    names = os.getenv("NAMES")
    rail_green_passes = os.getenv("RAIL_GREEN_PASSES")

    # Santa Apolinia Station Code: 94-30007
    # Coimbra-B Station Code: 94-36004

    # Separate Passengers Information
    logger.info("Separating passenger information")
    passengers, nr_passengers = separate_passengers(ids, names, rail_green_passes)
    buy_url = f"https://cp.pt/en/resultado-pesquisa?passageiros={nr_passengers}&selectedClass=2&startDate={departure_date}&departureStation={origin}&arrivalStation={destination}"

    try:
        page.goto(buy_url)
        if not login:
            logger.info("Rejecting cookies")
            page.locator("#onetrust-reject-all-handler").click()
    except Exception as e:
        logger.error(f"Error during navigation: {e}")

    
    logger.info("Selecting departure time %s", departure_time)
    page.locator("div").filter(
        has_text=re.compile(rf"^{departure_time}.*")) \
    .get_by_role("button").click()

    # Select Trip Button
    logger.info("Selecting trip")
    page.locator(".trip-Detail-info__detail-values__cta-button").click()
    # Buy Button
    page.locator(".search-results-page__footer__content__cta-button").click()

    page.locator(".checkbox-container").check()
    page.locator(".confirm-button").click()
    
    if not login: # If not logged in, continue as guest
        logger.info("Logging in as guest")
        page.locator(".guest-btn").click()

    # Fill Passenger Information
    logger.info("Filling passenger information")
    page.get_by_role("textbox", name="Email *").fill(email)

    for i, passenger in enumerate(passengers):
        logger.info(f"Configuring passenger {passenger['name']}")
        configure_passage(page, passenger)
        if i < nr_passengers - 1:
            page.get_by_role("button", name="Show").click()

    # Continue Purchase
    page.get_by_role("button", name="Next").click()
    page.get_by_role("button", name="Next").click()

    # Finalize Purchase
    page.get_by_role("button", name="Proceed to Payment").click()
    # Buys the ticket
    if os.getenv("DRY_RUN", "True").lower() in ('true', '1', 't'):
        logger.info("Dry run complete. Ticket not purchased.")
    else:
        logger.info("Buying tickets")
        page.get_by_role("button", name="Confirm").click()
        logger.info("Tickets bought successfully.")
        from time import sleep
        sleep(5)

def main():
    load_dotenv()
    email = os.getenv("EMAIL")

    slow_mo = int(os.getenv("SLOW_MO"))
    headless = os.getenv("HEADLESS", "False").lower() in ('true', '1', 't')
    login = os.getenv("LOGIN", "False").lower() in ('true', '1', 't')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless,  slow_mo=slow_mo)
        page = browser.new_page()

        if login:
            logger.info("Going to https://cp.pt/en")
            page.goto("https://cp.pt/en")
            logger.info("Rejecting cookies")
            page.locator("#onetrust-reject-all-handler").click()
            login_user(page, email)

        buy_ticket(page, email, login)

        browser.close()


if __name__ == "__main__":
    main()