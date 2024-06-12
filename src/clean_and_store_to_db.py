import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

def get_env_var(var_name):
    return os.getenv(var_name)

def clean_data(data):
    # Remove duplicates
    data.drop_duplicates(inplace=True)

    # Handle missing values (example: fill with a placeholder or remove)
    data.fillna('missing', inplace=True)

    # Standardize formats (example: date format)
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'], errors='coerce')

    # Validate data (example: ensure phone number column contains valid numbers)
    if 'phone_number' in data.columns:
        data['phone_number'] = data['phone_number'].apply(lambda x: x if x.isdigit() else 'invalid')

    return data

def combine_and_clean_data(directory):
    combined_data = pd.DataFrame()

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path)
            cleaned_data = clean_data(data)
            combined_data = pd.concat([combined_data, cleaned_data], ignore_index=True)
    
    return combined_data

def store_data_to_postgresql(data):
    # Database connection parameters
    user = get_env_var('POSTGRES_USER')
    password = get_env_var('POSTGRES_PASSWORD')
    db = get_env_var('POSTGRES_DB')
    host = get_env_var('POSTGRES_HOST')
    port = get_env_var('POSTGRES_PORT')

    # Create SQLAlchemy engine
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

    # Store data to PostgreSQL table
    data.to_sql('telegram_data', engine, if_exists='replace', index=False)
    print('Data stored in PostgreSQL successfully.')

