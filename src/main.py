from scrapper import scrape_telegram_channels
from utils import load_env_vars
from clean_and_store_to_db import combine_and_clean_data, store_data_to_postgresql

def main():
    load_env_vars()
    #scrape_telegram_channels()
    
    # Specify the directory containing the individual CSV files
    data_directory = 'data'

    # Combine and clean the data from all CSV files in the directory
    combined_cleaned_data = combine_and_clean_data(data_directory)
    print(combined_cleaned_data.head())

    # Store combined and cleaned data to PostgreSQL
    store_data_to_postgresql(combined_cleaned_data)

    # Save combined data to a single CSV file
    combined_cleaned_data.to_csv('data/combined_telegram_data.csv', index=False)
    print('Combined data saved to combined_telegram_data.csv')

if __name__ == "__main__":
    main()