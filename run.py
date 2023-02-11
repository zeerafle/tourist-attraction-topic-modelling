from trip_adivsor.utils import open_csv
from trip_adivsor.trip_advisor import TripAdvisor
from trip_adivsor.constants import REVIEWS_DATA_PATH, PLACES_DATA_PATH

with TripAdvisor() as ta:
    # open file
    places_writer = open_csv(
        PLACES_DATA_PATH,
        fieldnames=['id', 'name', 'rating']
    )
    places_writer.writeheader()
    reviews_writer = open_csv(
        REVIEWS_DATA_PATH,
        fieldnames=['place_id', 'title', 'description', 'rating'],
        delimiter='\t'
    )
    reviews_writer.writeheader()

    ta.get_page()
    places_links = ta.get_places()
    for place in places_links:
        places_writer.writerow(
            ta.get_places_details(place)
        )
        ta.get_reviews(reviews_writer)