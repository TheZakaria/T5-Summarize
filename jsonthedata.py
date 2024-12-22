import os
import json
import re
import unicodedata

# Define paths
root_dir = './EASC-UTF-8/Articles/'
output_file = 'summarization_dataset.json'

# Initialize an empty dataset
dataset = []

# Function to normalize line endings
def normalize_line_endings(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')

# Function to clean text and handle invisible characters
def clean_text(text):
    # Normalize Unicode characters to a consistent form
    text = unicodedata.normalize("NFKC", text)
    
    # Remove non-printable control characters (excluding Arabic characters and common punctuation)
    text = re.sub(r'[^\x20-\x7E\n\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]', '', text)
    
    return text

# Sort the directories numerically (if they are numeric)
folder_list = sorted(os.listdir(root_dir), key=lambda x: int(x) if x.isdigit() else x)
print(f"Total folders found: {len(folder_list)}")

for folder in folder_list:
    print(f"Processing folder: {folder}")  # Debugging line to see folder names
    folder_path = os.path.join(root_dir, folder)

    if os.path.isdir(folder_path):  # Ensure it's a directory
        article = None
        summaries = {}

        # Process all files in the folder
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            if file.endswith('.txt'):  # Identify the article
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
                    article = clean_text(normalize_line_endings(raw_content))  # Normalize line endings and clean
            else:  # Treat other files as summaries
                print(f'In {file_path} processing {file}')
                summary_key = file.split('.')[-1]  # Extract the last part (e.g., "A", "B")
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
                    summaries[summary_key] = clean_text(normalize_line_endings(raw_content))  # Normalize line endings and clean

        # Add to dataset if article and summaries exist
        if article and len(summaries) == 5:  # Ensure all 5 summaries are present
            dataset.append({
                'article': article,
                'summaries': summaries
            })

# Save the dataset as a JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)

print(f"Dataset saved to {output_file}")
