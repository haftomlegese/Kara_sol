import os
import logging
import cv2
import torch
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql


# Load environment variables from .env file
load_dotenv()

def get_env_var(var_name):
    return os.getenv(var_name)

# Configure logging
logging.basicConfig(
    filename='object_detection.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

logging.info('Object detection process started')

# Database connection
try:
    conn = psycopg2.connect(
        dbname="kera_db",
        user = get_env_var('POSTGRES_USER'),
        password = get_env_var('POSTGRES_PASSWORD'),
        host = get_env_var('POSTGRES_HOST'),
        port = get_env_var('POSTGRES_PORT')
    )
    cur = conn.cursor()
    logging.info('Connected to the PostgreSQL database')
except Exception as e:
    logging.error(f"Error connecting to the database: {str(e)}")
    raise

# Create table if it doesn't exist
try:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS object_detections (
        image_name TEXT,
        class_name TEXT,
        confidence FLOAT,
        x_min FLOAT,
        y_min FLOAT,
        x_max FLOAT,
        y_max FLOAT
    )
    """)
    conn.commit()
    logging.info('Table created or verified successfully')
except Exception as e:
    logging.error(f"Error creating/verifying table: {str(e)}")
    raise

# Load YOLOv5 model
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    logging.info('YOLOv5 model loaded successfully')
except Exception as e:
    logging.error(f"Error loading YOLO model: {str(e)}")
    raise

# Directory containing images
image_dir = 'media'
output_dir = 'data/output'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each image
for image_name in os.listdir(image_dir):
    try:
        # Load image
        image_path = os.path.join(image_dir, image_name)
        image = cv2.imread(image_path)
        logging.info(f"Processing image: {image_name}")

        # Perform object detection
        results = model(image)

        # Save results
        results.save(output_dir)

        # Extract relevant data
        detections = results.pandas().xyxy[0]  # Pandas DataFrame with detection results
        for index, row in detections.iterrows():
            try:
                cur.execute(
                    sql.SQL("INSERT INTO object_detections (image_name, class_name, confidence, xmin, ymin, xmax, ymax) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
                    [image_name, row['name'], row['confidence'], row['xmin'], row['ymin'], row['xmax'], row['ymax']]
                )
            except Exception as e:
                logging.error(f"Error inserting detection result into database for image {image_name}: {str(e)}")

        conn.commit()
        logging.info(f"Detection results stored in database for image: {image_name}")

    except Exception as e:
        logging.error(f"Error processing image {image_name}: {str(e)}")

# Close database connection
try:
    cur.close()
    conn.close()
    logging.info('Database connection closed')
except Exception as e:
    logging.error(f"Error closing the database connection: {str(e)}")

logging.info('Object detection process completed')