import json
import pandas as pd
import os

def convert_json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    combined_data = []
    
    for channel_data in data:
        channel_name = channel_data['channel']
        
        for message in channel_data['messages']:
            message['channel'] = channel_name
            combined_data.append(message)
    
    combined_df = pd.DataFrame(combined_data)
    
    # Saving combined data to a single CSV file
    combined_df.to_csv(csv_file_path, index=False, encoding='utf-8')

    print(f"Combined data saved to {csv_file_path}")

def main():
    json_file_path = os.path.join('data', 'scraped_data.json')
    csv_file_path = os.path.join('data', 'scraped_data.csv')
    
    convert_json_to_csv(json_file_path, csv_file_path)

if __name__ == "__main__":
    main()