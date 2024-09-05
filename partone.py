import pandas as pd
import re


def clean_name(name):

    return re.sub(r'[^a-zA-Z0-9]', '', name)


def generate_unique_email(df):

    email_counter = {}
    emails = []

    for index, row in df.iterrows():
        student_name = row['Student Name']
        if pd.isna(student_name):
            emails.append('')
            continue

        # Extract names and clean them
        names = [clean_name(part) for part in student_name.split(',')]

        if len(names) == 1:
            first_name = names[0]
            last_name = ''
        elif len(names) == 2:
            first_name, last_name = names
        else:
            first_name = names[0]
            last_name = ' '.join(names[1:])

        # Create base email
        if first_name:
            email_base = f"{first_name[0].lower()}{last_name.lower()}"
        else:
            email_base = f"{last_name.lower()}"

        #  uniqueness
        if email_base in email_counter:
            email_counter[email_base] += 1
            email = f"{email_base}{email_counter[email_base]}@strathmore.edu"
        else:
            email_counter[email_base] = 0
            email = f"{email_base}@strathmore.edu"

        emails.append(email)

    return emails



file_path = r'C:\Users\KE\Downloads\Test Files.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')


print(df.head())

# Check if 'Student_Name' is really there or not
if 'Student Name' in df.columns:

    df['email'] = generate_unique_email(df)


    print(df[['Student Name', 'email']])
else:
    print("The 'Student Name' column is missing from the file.")
import pandas as pd
import re


def clean_name(name):

    return re.sub(r'[^a-zA-Z0-9]', '', name)


def generate_unique_email(df):

    email_counter = {}
    emails = []

    for index, row in df.iterrows():
        student_name = row['Student Name']
        if pd.isna(student_name):
            emails.append('')
            continue

        # Extract names and clean them
        names = [clean_name(part) for part in student_name.split(',')]

        if len(names) == 1:
            first_name = names[0]
            last_name = ''
        elif len(names) == 2:
            first_name, last_name = names
        else:
            first_name = names[0]
            last_name = ' '.join(names[1:])

        # Create base email
        if first_name:
            email_base = f"{first_name[0].lower()}{last_name.lower()}"
        else:
            email_base = f"{last_name.lower()}"

        #  uniqueness
        if email_base in email_counter:
            email_counter[email_base] += 1
            email = f"{email_base}{email_counter[email_base]}@strathmore.edu"
        else:
            email_counter[email_base] = 0
            email = f"{email_base}@strathmore.edu"

        emails.append(email)

    return emails



file_path = r'C:\Users\KE\Downloads\Test Files.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')


print(df.head())

# Check if 'Student_Name' is really there or not
if 'Student Name' in df.columns:

    df['email'] = generate_unique_email(df)


    print(df[['Student Name', 'email']])
else:
    print("The 'Student Name' column is missing from the file.")
