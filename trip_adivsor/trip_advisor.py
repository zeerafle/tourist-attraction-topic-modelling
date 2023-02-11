import re
import os
import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import constants as c
from .utils import open_csv


class TripAdvisor(webdriver.Firefox):
    def __init__(self, webdriver_path=r'C:\SeleniumDriver', teardown=False):
        self.webdriver_path = webdriver_path
        self.teardown = teardown
        os.environ['PATH'] += r'C:\SeleniumDriver'
        super(TripAdvisor, self).__init__()
        self.implicitly_wait(5)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_page(self):
        self.get(c.BASE_URL)

    def get_places(self):
        places = self.find_elements(By.XPATH, "//*[@class='alPVI eNNhq PgLKC tnGGX']")
        places_links = []
        for place in places:
            places_links.append(
                place.find_element(By.TAG_NAME, 'a').get_attribute('href')
            )
        return places_links

    def get_places_details(self, url):
        self.get(url)
        id = re.search(r'[a-z]\d+-[a-z]\d+', url)
        name = self.find_element(By.TAG_NAME, 'h1').text
        rating = self.find_element(By.CSS_SELECTOR, "div[aria-label*='reviews']").get_attribute('aria-label')[:3]
        rating = float(rating)
        print('getting', name)
        return {
            'id': id.group(0),
            'name': name,
            'rating': rating
        }

    def get_reviews(self, reviews_writer):
        # some places have many reviews that it needs pagination
        # while the next page button exist click that,
        # if not set next_page_available to false so the loop stops
        next_page_available = True
        page_num = 1
        while next_page_available:
            print('page', page_num)
            id = re.search(r'[a-z]\d+-[a-z]\d+', self.current_url)
            all_reviews_container = self.find_element(By.CLASS_NAME, 'LbPSX')
            reviews_divs = all_reviews_container.find_elements(By.XPATH, './*')
            reviews_divs = reviews_divs[:-1] # the last one is not the review

            review_num = 1
            for review in reviews_divs:
                print('review', review_num)
                review_rating = float(
                    review.find_element(
                        By.CSS_SELECTOR, 'svg[aria-label$="bubbles"]'
                    ).get_attribute('aria-label')[:3]
                )
                review_title = review.find_element(By.CSS_SELECTOR, 'a[href^="/ShowUserReviews"]').text
                print('getting review:', review_title)
                review_description = review.find_element(By.XPATH, 'div/div/div[5]').text\
                    .replace('\n', '')\
                    .rstrip('Read more') # some really long review will include the read more button
                reviews_writer.writerow({
                    'place_id': id.group(0),
                    'title': review_title,
                    'description': review_description,
                    'rating': review_rating
                })
                review_num += 1

            # check if next page button is available
            try:
                next_page = WebDriverWait(self, 1).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'a[aria-label="Next page"]')
                    )
                )
                next_page.click()
                time.sleep(3.0)
            except:
                next_page_available = False

            page_num += 1
