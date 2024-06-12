import logging

def setup_logging():
    logging.basicConfig(
        filename='scraper.log',
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )