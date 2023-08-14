from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

page_to_check = ["https://www.recreation.gov/camping/campgrounds/232464",
                 "https://www.recreation.gov/camping/campgrounds/259084"]


def main():
    # driver = webdriver.Firefox()
    driver = webdriver.Chrome()

    try:
        while True:
            for page in page_to_check:
                driver.get(page)

                for availability in driver.find_elements(By.CLASS_NAME, "rec-availability-date"):
                    if availability.text == "A":
                        if "Aug 19" in availability.accessible_name:
                            print("Found availability!")
                            print(availability.accessible_name)
                            while True:
                                os.system('play -nq -t alsa synth {} sine {}'.format(1, 440))
                                time.sleep(1)
            time.sleep(30)
    except KeyboardInterrupt:
        print("Exiting...")
        driver.close()
        driver.quit()
        exit(0)


if __name__ == '__main__':
    main()