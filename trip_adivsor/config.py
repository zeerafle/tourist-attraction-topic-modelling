import os
from dotenv import load_dotenv

# load env
load_dotenv()

SCRAPE_DO_KEY = os.getenv('SCRAPE_DO_KEY')
