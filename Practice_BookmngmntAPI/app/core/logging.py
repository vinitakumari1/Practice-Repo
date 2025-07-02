import logging
import json
import os

# Logging setup
logging.basicConfig(
    filename='book.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


BOOK_FILE = r'C:\Agentic-AI Trainings\Practice\app\db\books.json'

def load_books():
    if not os.path.exists(BOOK_FILE):
        logger.warning("books.json not found.")
        return []
    with open(BOOK_FILE, 'r') as f:
        logger.info("Loaded books from JSON.")
        return json.load(f)

def save_books(data):
    with open(BOOK_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        logger.info("Saved books to JSON.")
