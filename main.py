from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from sys import platform

if platform == "win32":
    from win10toast import ToastNotifier


page_to_check = ["https://www.recreation.gov/camping/campgrounds/232464",
                 "https://www.recreation.gov/camping/campgrounds/259084"]


account_email = ""
account_password = ""
assert account_email != "" and account_password != "", "Please fill in account_email and account_password"


def main():
    if platform == "win32":
        toast = ToastNotifier()
        toast.show_toast(
            "Start",
            "Looking for camp",
            duration=10,
            # icon_path="icon.ico",
            # threaded=True,
        )

    # driver = webdriver.Firefox()
    # driver = webdriver.Chrome()
    driver = webdriver.Edge()

    # login recreation.gov
    driver.get("https://www.recreation.gov")

    driver.find_element(By.ID, "ga-global-nav-log-in-link").click()
    driver.find_element(By.ID, "email").send_keys(account_email)
    driver.find_element(By.ID, "rec-acct-sign-in-password").send_keys(account_password)

    for button in driver.find_elements(By.CLASS_NAME, "rec-acct-sign-in-btn"):
        if "Log In" in button.text:
            button.click()
            break
    else:
        print("Failed to find login button")
        exit(1)

    time.sleep(1)

    try:
        while True:
            for page in page_to_check:
                print("Checking page: " + page)
                driver.get(page)
                print("Loaded page: " + driver.title)

                for availability in driver.find_elements(By.CLASS_NAME, "rec-availability-date"):
                    if availability.text == "A":
                        if "Aug 19" in availability.accessible_name:
                            print("Found availability!")
                            print(availability.accessible_name)

                            availability.click()

                            buttons = driver.find_elements(By.CLASS_NAME, "availability-page-book-now-button-tracker")

                            for button in buttons:
                                if "Add to Cart" in button.text:
                                    button.click()
                                    break
                            else:
                                print("Failed to find add to cart button")

                            while True:
                                if platform != "win32":
                                    os.system('play -nq -t alsa synth {} sine {}'.format(1, 440))
                                    time.sleep(1)
                                else:
                                    toast.show_toast(
                                        "Camp Found!",
                                        availability.accessible_name,
                                        duration=1,
                                        # threaded=True,
                                    )
                                time.sleep(2)

            time.sleep(30)
    except KeyboardInterrupt:
        print("Exiting...")
        driver.quit()
        exit(0)


if __name__ == '__main__':
    main()