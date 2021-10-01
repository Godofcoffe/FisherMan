#! /usr/bin/env python3

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://facebook.com/"
EMAIL = "*EMAIL HERE*"
PASSWORD = "*PASSWORD HERE*"

brw = Firefox()
wbw = WebDriverWait(brw, 5)
brw.get(URL)
email = wbw.until(ec.element_to_be_clickable((By.NAME, "email")))
pwd = wbw.until(ec.element_to_be_clickable((By.NAME, "pass")))
ok = wbw.until(ec.element_to_be_clickable((By.NAME, "login")))
email.send_keys(EMAIL)
pwd.send_keys(PASSWORD)
ok.click()

print("""
    URL = variable of the facebook url: https://facebook.com/
    EMAIL = email variable in the code
    PASSWORD = password variable
    brw = instance of Firefox()
""")
