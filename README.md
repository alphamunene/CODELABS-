# CODELABS-
Student Email Address Generator,gender categorising and Google Drive Backup
Overview
This project involves generating unique email addresses for students, analyzing names to identify special characters, and computing name similarities using LaBSE. Additionally, it includes uploading the generated files to Google Drive for backup.

Features
Generate Unique Email Addresses: Create unique email addresses for students based on their names.
Identify Special Characters: Detect names with special characters using regular expressions.
Compute Name Similarities: Use LaBSE to find and filter name similarities between male and female students.
File Management: Merge documents, shuffle names, and save the results in JSON and JSONL formats.
Backup to Google Drive: Upload files to Google Drive using the Google Drive API.

Prerequisites
Python 3.x: Ensure you have Python 3.x installed on your system or
Pycharm

Required Python Packages:
pandas
openpyxl
transformers
sentence-transformers
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client

Install these packages using pip in the terminal or via packages:

pip install pandas openpyxl transformers sentence-transformers google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

functions.py: Contains functions for generating email addresses, finding names with special characters, and computing name similarities.
main.py: The main script that processes data, generates email addresses, and saves output files.
upload_to_drive.py: Script for uploading files to Google Drive.
students.xlsx: Sample data file.
credentials.json: OAuth 2.0 credentials file for Google API (place this in the same directory).
Output Files
output_files/shuffled_data.json: JSON file with shuffled student data.
output_files/shuffled_data.jsonl: JSONL file with shuffled student data.
output_files/similarities.json: JSON file with name similarity results.
output_files/special_char_names.txt: Text file listing names with special characters.
Logs: Contains log files with processing details.
Troubleshooting
File Not Found Errors: Ensure all file paths in the script are correctly set and files exist in the specified locations.
API Authentication Issues: Verify credentials.json is correctly placed and OAuth 2.0 authentication is completed.
