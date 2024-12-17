# Gracenote Schedule Downloader and Uploader

This project automates the process of downloading schedule reports from the Gracenote platform using Selenium and uploading them to AWS S3 and Google Drive. The tool is designed to handle multiple call sign IDs, ensuring efficient file management.

---

## Features
- Automates login and navigation on the Gracenote platform.
- Downloads schedule reports for multiple call sign IDs.
- Uploads downloaded files to:
  - **AWS S3 Bucket**
  - **Google Drive Folder**
- Ensures robust error handling and logging.

---

## Requirements
### **1. Python Dependencies**
Install the required Python libraries:
```bash
pip install selenium boto3 google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


