import os
import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory of the script
config_file_path = os.path.join(current_dir, 'config1.ini')  # Change the trailing number for each profile.
config = configparser.ConfigParser()  # Create a ConfigParser instance
config.read(config_file_path)  # Read the config.ini file

driver = webdriver.Chrome()
driver.set_window_size(400, 800)

USERNAME = config['USER_CREDENTIALS']['USERNAME']
PASSWORD = config['USER_CREDENTIALS']['PASSWORD']
CALL_SIGN_ID = config['USER_CREDENTIALS']['CALL_SIGN_ID']
CALL_SIGN_ID_LIST = config['USER_CREDENTIALS']['CALL_SIGN_ID_LIST']
GRACENOTE_URL = config['GRACENOTE_CREDS']['GRACENOTE_URL']


# Open the URL
driver.get(GRACENOTE_URL)

try:

    # Wait for the email input field to be visible and interactable
    wait = WebDriverWait(driver, 10)  # 10 seconds timeout
    email_field = wait.until(EC.element_to_be_clickable((By.ID, "signInFormUsername")))

    # Enter the email
    email_field.send_keys(f"{USERNAME}")

    password_field = wait.until(EC.element_to_be_clickable((By.ID, "signInFormPassword")))
    password_field.send_keys(f"{PASSWORD}")

    login_button = wait.until(EC.element_to_be_clickable((By.NAME, "signInSubmitButton")))
    login_button.click()

    driver.set_window_size(1400, 800)

    select_next_week = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="single-spa-application:@gracenote/gnview-webclient"]/div/div/div[2]/div/div[1]/div[2]/div[1]/span/div/label[3]/span')))

    # Wait for 5 seconds to observe the result
    time.sleep(1)
    select_next_week = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="single-spa-application:@gracenote/gnview-webclient"]/div/div/div[2]/div/div[1]/div[2]/div[1]/span/div/label[3]/span')))
    select_next_week.click()
    time.sleep(1)
    ch_call_sign_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="single-spa-application:@gracenote/gnview-webclient"]/div/div/div[2]/div/div[1]/div[2]/span/div/label[2]')))
    ch_call_sign_button.click()
    time.sleep(1)

    enter_ch_sign_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="single-spa-application:@gracenote/gnview-webclient"]/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div/input[1]')))
    enter_ch_sign_field.send_keys(CALL_SIGN_ID)

    dropdown_item = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="async-typeahead--item-0"]/a')))
    dropdown_item.click()

    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="single-spa-application:@gracenote/gnview-webclient"]/div/div/div[2]/div/div[1]/div[2]/div[3]/button')))
    search_button.click()

    save_csv = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="single-spa-application:@gracenote/gnview-webclient"]/div/div/div[2]/div/div[1]/div[1]/div[3]/button')))
    save_csv.click()

    time.sleep(10)

finally:
    driver.quit()