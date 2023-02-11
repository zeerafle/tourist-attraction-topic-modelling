from trip_adivsor import config as c
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
REVIEWS_DATA_PATH = os.path.join(ROOT, 'data', 'reviews.csv')
PLACES_DATA_PATH = os.path.join(ROOT, 'data', 'places.csv')
BASE_URL = 'https://www.tripadvisor.com/Attractions-g2301802-Activities-oa0-East_Kalimantan_Kalimantan.html'
SCRAPE_URL = f'http://api.scrape.do?token={c.SCRAPE_DO_KEY}&url={BASE_URL}'