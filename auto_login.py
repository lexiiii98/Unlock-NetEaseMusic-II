# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "007EEF5D7FB9F4F22ED090A4A2B27C32A47AAF5331C301357E6812E88341116C71480E5F54E2FBA729E7A17199FDD9CB08936A527E49171E893004E956955ABFC8C6298AB1FEE1B8AC312F3559393B71358157C7492E7A3BBDA44354318E23F20B5A9D2E5C327AA56A770243B15E90A10082CB323A6D107F51E64ED994C1CC7CE8D84607CE833C5A44E0B3284B831DCECDB9CE0A2AAD1BCF8296139EB7AF4F3DC07F2814066060F36796ECFD154048E88081B2A3FDA9BE3E5182D2F7EB804F91AB51CEEB868B27407FB9700D0F2E6155F43DD47C718616225CAA34EA5FD912BBD7F957568599042826CCB613BDA395888079598AF1EB56C69C73AFD1306C56CC84FDB47019304233AB1796113E93147B60A172C710488B27D0B2C6B2CAC40FEB9D6C0875B686FA96EDB26F3C550F9283A2FEAA5805D7642CCF923C04D59D04340E85648CA371221CFE1B4EF9CC73847B70"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
