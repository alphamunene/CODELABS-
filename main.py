import pandas as pd
import os
import re
import json

from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer, util


# Function to load the LaBSE model
def load_laBSE_model():
    model_name = 'sentence-transformers/LaBSE'
    model = SentenceTransformer(model_name)
    return model


# Function to generate email addresses
def generate_email_addresses(df):
    emails = []
    seen_emails = set()

    for name in df['Student Name']:
        if ',' in name:
            last_name, first_middle_names = name.split(',', 1)
        else:
            last_name, first_middle_names = name, ""

        first_middle_names = first_middle_names.strip().split()
        first_name_letter = first_middle_names[0][0].lower() if len(first_middle_names) > 0 else ''
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


# Function to identify names with special characters
def find_names_with_special_characters(names):
    special_char_pattern = re.compile(r'[^a-zA-Z\s]')
    return [name for name in names if special_char_pattern.search(name)]


# Function to compute similarity between male and female names using LaBSE
def compute_name_similarities(male_names, female_names, model):
    male_embeddings = model.encode(male_names, convert_to_tensor=True)
    female_embeddings = model.encode(female_names, convert_to_tensor=True)

    similarities = []
    for i, male_embedding in enumerate(male_embeddings):
        similarities.append({
            'male_name': male_names[i],
            'similarities': [
                {
                    'female_name': female_names[j],
                    'similarity_score': float(util.pytorch_cos_sim(male_embedding, female_embeddings[j]))
                }
                for j in range(len(female_names))
            ]
        })

    # Filter for at least 50% similarity
    filtered_similarities = [
        {
            'male_name': sim['male_name'],
            'similarities': [
                sim_score for sim_score in sim['similarities'] if sim_score['similarity_score'] >= 0.5
            ]
        }
        for sim in similarities
    ]

    return filtered_similarities


def main():
    # Define file path and output directory
    file_path = 'students.xlsx'
    output_dir = 'output_files'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load data
    df = pd.read_excel(file_path)

    # Generate email addresses
    emails = generate_email_addresses(df)
    df['Email'] = emails

    # Identify gender-based lists (assuming a column 'Gender' is present)
    if 'Gender' in df.columns:
        male_df = df[df['Gender'].str.lower() == 'male']
        female_df = df[df['Gender'].str.lower() == 'female']
        male_names = male_df['Student Name'].tolist()
        female_names = female_df['Student Name'].tolist()
    else:
        print("Error: 'Gender' column not found in the data.")
        return

    # Log counts
    with open(os.path.join(output_dir, 'process.log'), 'w') as log_file:
        log_file.write(f"Number of Male Students: {len(male_names)}\n")
        log_file.write(f"Number of Female Students: {len(female_names)}\n")

    # Find names with special characters
    special_char_names = find_names_with_special_characters(df['Student Name'])
    with open(os.path.join(output_dir, 'special_char_names.txt'), 'w') as sc_file:
        sc_file.write("\n".join(special_char_names))

    # Load LaBSE model
    model = load_laBSE_model()

    # Compute name similarities
    similarities = compute_name_similarities(male_names, female_names, model)

    # Save similarities to JSON
    with open(os.path.join(output_dir, 'similarities.json'), 'w') as json_file:
        json.dump(similarities, json_file, indent=4)

    # Merge all documents
    df_combined = pd.concat([male_df, female_df], ignore_index=True)


    df_combined = df_combined.sample(frac=1).reset_index(drop=True)
    df_combined.to_json(os.path.join(output_dir, 'shuffled_data.json'), orient='records', lines=False)
    df_combined.to_json(os.path.join(output_dir, 'shuffled_data.jsonl'), orient='records', lines=True)


if __name__ == "__main__":
    main()
