import argparse
import locale
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

parser = argparse.ArgumentParser(
    description="This script will book you the next available appointment at a Bürgeramt (citizen's office) in Berlin."
)
parser.add_argument("--name", required=True, help="Your name")
parser.add_argument("--email", required=True, help="Your email address")
parser.add_argument("--phone", help="Your phone number")
parser.add_argument("--id", required=True, help="Service ID")
parser.add_argument(
    "--start_date",
    default=datetime.now().strftime("%d.%m.%Y"),
    help="Start day for booking appointments (format: \"DD.MM.YYYY\"), default: current day)",
)
parser.add_argument(
    "--end_date", help="End day for booking appointments (format: \"DD.MM.YYYY\")"
)
args = parser.parse_args()

your_name = args.name
your_email = args.email
your_phone = args.phone
dienstleistung_id = args.id
start_date = args.start_date
end_date = args.end_date


def run_script():
    url = (
        f"https://service.berlin.de/terminvereinbarung/termin/all/{dienstleistung_id}/"
    )

    options = webdriver.ChromeOptions()

    browser = webdriver.Chrome(options=options)
    browser.get(url)

    current_url = browser.current_url

    return current_url, browser


def click_first_link(browser, class_name):
    try:
        link_selector = f"//td[contains(@class, '{class_name}')]//a"
        link_element = browser.find_element(By.XPATH, link_selector)
        link_element.click()
        return True
    except:
        return False


def get_next_available_day(browser, start_date, end_date):
    available_days = browser.find_elements(
        By.XPATH, "//td[contains(@class, 'buchbar')]//a"
    )
    start_date = datetime.strptime(start_date, "%d.%m.%Y")

    if end_date:
        end_date = datetime.strptime(end_date, "%d.%m.%Y")

    for day_element in available_days:
        day_text = day_element.get_attribute("aria-label")
        day_date_str = day_text.split(" - ")[0]
        day_date = datetime.strptime(day_date_str, "%d.%m.%Y")

        if not end_date or (end_date and day_date <= end_date):
            if day_date >= start_date:
                return day_element

    return None


def fill_and_submit_form(browser):
    family_name_input = browser.find_element(By.ID, "familyName")
    family_name_input.send_keys(your_name)

    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys(your_email)

    emailequality_input = browser.find_element(By.ID, "emailequality")
    emailequality_input.send_keys(your_email)

    try:
        phone_input = browser.find_element(By.ID, "telephone")
        phone_input.send_keys(your_phone)
    except:
        pass

    try:
        # Optionally opt out of survey if the question is present
        survey_opt_in_select_element = browser.find_element_by_name("surveyAccepted")
        select = Select(survey_opt_in_select_element)
        select.select_by_value("0")
    except:
        pass

    agb_checkbox = browser.find_element(By.ID, "agbgelesen")
    browser.execute_script("arguments[0].click();", agb_checkbox)

    time.sleep(50)

    register_submit_button = browser.find_element(By.ID, "register_submit")
    browser.execute_script("arguments[0].click();", register_submit_button)


def main():
    while True:
        print("Script is running...")
        result, browser = run_script()
        time.sleep(20)
        if result == "https://service.berlin.de/terminvereinbarung/termin/taken/":
            print("No available dates, try again...")
        else:
            print("Available appointment found.")
            next_available_day = get_next_available_day(browser, start_date, end_date)
            if next_available_day:
                next_available_day.click()
                print(f"Date {start_date} or later selected.")
                if click_first_link(browser, "frei"):
                    print("Time selected.")
                    time.sleep(25)
                    fill_and_submit_form(browser)
                    print("Form filled in and sent.")
                    time.sleep(5)
                    break
                else:
                    print(
                        "The free appointment is no longer available. A new attempt will be started."
                    )
            else:
                print(
                    "No available appointment from the specified start day. A new attempt will be started."
                )


if __name__ == "__main__":
    main()
