import re
import os
from time import sleep
from dotenv import load_dotenv
from playwright.sync_api import Page, sync_playwright

def login(page: Page, username):
    password = os.getenv("PASSWORD")
    
    page.goto("https://cp.pt/en")
    page.locator("#onetrust-reject-all-handler").click()
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

def separate_passengers(nr_passengers, ids, names, rail_green_passes):

    ids = ids.split(",")
    names = names.split(",")
    rail_green_passes = rail_green_passes.split(",")

    passengers = []
    for i in range(nr_passengers):
        passenger = {
            "id": ids[i].strip(),
            "name": names[i].strip(),
            "rail_green_pass": rail_green_passes[i].strip()
        }
        passengers.append(passenger)

    return passengers


def buy_ticket(page: Page, email):
    nr_passengers = int(os.getenv("NR_PASSENGERS"))
    origin = os.getenv("ORIGIN")
    destination = os.getenv("DESTINATION")
    departure_date = os.getenv("DEPARTURE_DATE")
    departure_time = os.getenv("DEPARTURE_TIME")
    ids = os.getenv("IDS")
    names = os.getenv("NAMES")
    rail_green_passes = os.getenv("RAIL_GREEN_PASSES")

    # Separate Passengers Information
    passengers = separate_passengers(nr_passengers, ids, names, rail_green_passes)


    page.goto("https://cp.pt/en")
    

    # Set Departure Date
    page.locator('#ida').fill(departure_date)
    # Set Origin
    page.get_by_role("textbox", name="From").fill(origin)
    page.get_by_role("combobox", name=origin).locator("ul").click()
    # Set Destination
    page.get_by_role("textbox", name="To").fill(destination)
    page.get_by_role("combobox", name=destination).locator("ul").click()

    # Select Number of Passengers
    if nr_passengers > 1:
        page.get_by_role("button", name="1 passenger(s)").click()
        for _ in range(nr_passengers - 1):
            page.get_by_role("button", name="Increase").click()


    # Proceed to next screen
    page.get_by_role("button", name="Search").click()

    # Select Departure Time
    page.locator("div").filter(
        has_text=re.compile(rf"^{departure_time}.*")) \
    .get_by_role("button").click()

    # Select Trip Button
    page.locator(".trip-Detail-info__detail-values__cta-button").click()
    # Buy Button
    page.locator(".search-results-page__footer__content__cta-button").click()

    page.locator(".checkbox-container").check()
    page.locator(".confirm-button").click()
    page.locator(".guest-btn").click()

    # Fill Passenger Information
    page.get_by_role("textbox", name="Email *").fill(email)

    for i, passenger in enumerate(passengers):
        configure_passage(page, passenger)
        if i < nr_passengers - 1:
            page.get_by_role("button", name="Show").click()

    # Continue Purchase
    page.get_by_role("button", name="Next").click()
    page.get_by_role("button", name="Next").click()

    # Finalize Purchase
    page.get_by_role("button", name="Proceed to Payment").click()





def main():
    load_dotenv()
    email = os.getenv("EMAIL")

    slow_mo = int(os.getenv("SLOW_MO"))
    headless = os.getenv("HEADLESS", "False").lower() in ('true', '1', 't')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless,  slow_mo=slow_mo)
        page = browser.new_page()
        page.goto("https://cp.pt/en")
        # Close cookie banner
        page.locator("#onetrust-reject-all-handler").click()

        buy_ticket(page, email)

        browser.close()


if __name__ == "__main__":
    main()