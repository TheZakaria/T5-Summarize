import json
import csv

# Define file paths
input_json_file = 'summarization_dataset.json'
output_csv_file = 'summarization_dataset.csv'

# Load the JSON data
with open(input_json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Open the CSV file for writing with a custom delimiter
with open(output_csv_file, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='|')  # Use '|' as the delimiter
    
    # Write the header
    writer.writerow(['Article', 'Summary'])

    # Iterate over each entry in the JSON
    for entry in data:
        article = entry['article']
        summaries = entry['summaries']
        
        # Write each summary as a separate row
        for key, summary in summaries.items():
            writer.writerow([article, summary])

print(f"CSV file saved to {output_csv_file}")
