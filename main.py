import os
import time
import configparser
import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory of the script
config_file_path = os.path.join(current_dir, 'config.ini')  # Change the trailing number for each profile.
config = configparser.ConfigParser()  # Create a ConfigParser instance
config.read(config_file_path)  # Read the config.ini file
DOWNLOAD_DIR = "/Users/caglartogan/Downloads"  # Directory where files are saved
BUCKET_NAME = "tcl-north-america-content"
S3_BUCKET_PATH = "Content/CBS/Fast/"    

driver = webdriver.Chrome()
driver.set_window_size(400, 800)

# Initialize S3 Client
s3 = boto3.client('s3', region_name='us-east-1')

def upload_to_s3(file_path, bucket_name, s3_path):
    """Uploads a file to S3."""
    try:
        s3_key = os.path.join(s3_path, os.path.basename(file_path))
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {e}")
        
def authenticate_google_drive():
    """Authenticate the user and return credentials."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds        

def upload_to_google_drive(file_path, folder_id):
    """Uploads a file to Google Drive."""
    try:
        # Load credentials and create service
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE)
        service = build('drive', 'v3', credentials=creds)

        # File metadata
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype='application/vnd.ms-excel')

        # Upload file
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"Uploaded {file_path} to Google Drive with file ID: {file.get('id')}")
    except Exception as e:
        print(f"Failed to upload {file_path} to Google Drive: {e}")


USERNAME = config['USER_CREDENTIALS']['USERNAME']
PASSWORD = config['USER_CREDENTIALS']['PASSWORD']

CALL_SIGN_ID_LIST = config['USER_CREDENTIALS']['CALL_SIGN_ID_LIST'].split(", ")
GRACENOTE_URL = config['GRACENOTE_CREDS']['GRACENOTE_URL']
# Google Drive Setup
CREDENTIALS_FILE = '/Users/caglartogan/epg_downloads/gracenote-to-cloud/credentials.json'  # Path to your credentials.json file
FOLDER_ID = '1_gu6XJ5Dm9D8XWDRrwF_kjHev986AXZk'  # Google Drive folder ID



try:
     
# Open the URL
    driver.get(GRACENOTE_URL)

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
    
    for call_sign_id in CALL_SIGN_ID_LIST:

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
        enter_ch_sign_field.send_keys(call_sign_id)

        dropdown_item = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="async-typeahead--item-0"]/a')))
        dropdown_item.click()

        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="single-spa-application:@gracenote/gnview-webclient"]/div/div/div[2]/div/div[1]/div[2]/div[3]/button')))
        search_button.click()

        save_csv = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="single-spa-application:@gracenote/gnview-webclient"]/div/div/div[2]/div/div[1]/div[1]/div[3]/button')))
        save_csv.click()
        print(f"Downloaded file for CALL_SIGN_ID: {call_sign_id}")
        time.sleep(10)
        # Go back to the previous page
        driver.back()
        time.sleep(2)
    print("Uploading files to S3...")
    for file_name in os.listdir(DOWNLOAD_DIR):
        if file_name.startswith("schedule_report_") and file_name.endswith(".csv"):
            file_path = os.path.join(DOWNLOAD_DIR, file_name)
            upload_to_s3(file_path, BUCKET_NAME, S3_BUCKET_PATH)   
            
    # Upload all downloaded files to TCL Google Drive
    print("Uploading files to Google Drive...")
    for file_name in os.listdir(DOWNLOAD_DIR):
        if file_name.startswith("schedule_report_") and file_name.endswith(".csv"):
            file_path = os.path.join(DOWNLOAD_DIR, file_name)
            upload_to_google_drive(file_path, FOLDER_ID)             
        

        

finally:
    driver.quit()
    print("Script completed successfully!")
