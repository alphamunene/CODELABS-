
 # functions.py

import re


def generate_email_addresses(df):
    emails = []
    seen_emails = set()

    for name in df['Student Name']:
        # Split the name 
        if ',' in name:
            last_name, first_middle_names = name.split(',', 1)
        else:
            
            last_name, first_middle_names = name, ""

       
        first_middle_names = first_middle_names.strip().split()

        if len(first_middle_names) > 0:
            first_name_letter = first_middle_names[0][0].lower()
        else:
            first_name_letter = ''  #first/middle names are missing

        last_name_clean = re.sub(r'[^a-zA-Z0-9]', '', last_name.strip()).lower()
        first_name_letter_clean = re.sub(r'[^a-zA-Z0-9]', '', first_name_letter)

      
        base_email = f"{first_name_letter_clean}{last_name_clean}@gmail.com"

       
        email = base_email
        counter = 1
        while email in seen_emails:
            email = f"{first_name_letter_clean}{last_name_clean}{counter}@gmail.com"
            counter += 1

        seen_emails.add(email)
        emails.append(email)

    return emails
