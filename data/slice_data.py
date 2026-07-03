import json
import csv

# We removed "data/" because the script is already inside the data folder!
input_json_path = 'yelp_academic_dataset_review.json'
output_csv_path = 'yelp_small.csv'

print("Opening the massive Yelp file... Let's slice it down to size.")

with open(input_json_path, 'r', encoding='utf-8') as json_file, \
     open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
    
    writer = csv.writer(csv_file)
    writer.writerow(['Review'])
    
    count = 0
    for line in json_file:
        if count >= 5000: 
            break
            
        try:
            review_data = json.loads(line)
            review_text = review_data.get('text', '').strip()
            
            if review_text:
                writer.writerow([review_text])
                count += 1
                
                if count % 1000 == 0:
                    print(f"-> Extracted {count} reviews...")
        except Exception as e:
            continue

print(f"\nSuccess! Created a lightweight file at: {output_csv_path}")