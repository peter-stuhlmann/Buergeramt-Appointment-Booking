import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser(description="This script will book you the next available appointment at a Bürgeramt (citizen's office) in Berlin.")
parser.add_argument("--name", required=True, help="Your name")
parser.add_argument("--email", required=True, help="Your email address")
parser.add_argument("--id", required=True, help="Service ID")
args = parser.parse_args()

your_name = args.name
your_email = args.email
dienstleistung_id = args.id

def run_script():
    url = f"https://service.berlin.de/dienstleistung/{dienstleistung_id}/"
    link_selector = ".button.button--negative"

    options = webdriver.ChromeOptions()

    browser = webdriver.Chrome(options=options)
    browser.get(url)

    try:
        link_element = browser.find_element(By.CSS_SELECTOR, link_selector)
    except:
        try:
            link_element = browser.find_element(By.XPATH, "//a[contains(@class, 'button--negative')]")
        except:
            print("The link leading to the appointment booking was not found. Possibly its class has been changed.")
            return False, None

    try:
        link_element.click()
    except:
        try:
            browser.execute_script("arguments[0].click();", link_element)
        except:
            link_element.send_keys(Keys.ENTER)

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

def fill_and_submit_form(browser):
    family_name_input = browser.find_element(By.ID, "familyName")
    family_name_input.send_keys(your_name)

    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys(your_email)

    agb_checkbox = browser.find_element(By.ID, "agbgelesen")
    browser.execute_script("arguments[0].click();", agb_checkbox)

    time.sleep(10)

    register_submit_button = browser.find_element(By.ID, "register_submit")
    browser.execute_script("arguments[0].click();", register_submit_button)

def main():
    while True:
        print("Script is running...")
        result, browser = run_script()
        if result == "https://service.berlin.de/terminvereinbarung/termin/taken/":
            print("No available dates, try again...")
        else:
            print("Available appointment found.")
            if click_first_link(browser, "buchbar"):
                print("Date selected.")
                if click_first_link(browser, "frei"):
                    print("Time selected.")
                    fill_and_submit_form(browser)
                    print("Form filled in and sent.")
                    time.sleep(5)
                    break
                else:
                    print("The free appointment is no longer available. A new attempt will be started.")
            else:
                print("The free appointment is no longer available. A new attempt will be started.")

if __name__ == "__main__":
    main()