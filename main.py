# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# import time
# from selenium import webdriver
#
# driver = webdriver.Chrome('/Users/karolinaadelbergyte/Desktop/tools/chromedriver')  # Optional argument, if not specified will search path.
# driver.get('http://www.google.com/');
# time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!
# driver.quit()

import logging
import time
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters

# Change root logger level (default is WARN)
logging.basicConfig(level = logging.INFO)


def on_data(data: EventData):

    def _clear_string(txt):
        return txt.replace(" ", "_").replace("/", "").replace(",", "")

    path = "/Users/karolinaadelbergyte/Desktop/Projects/scraping/JobAds"
    file_name = f"{path}/{_clear_string(data.company)}_{_clear_string(data.title)}_{_clear_string(data.date)}_{int(time.time()*10000)}.txt"
    file_content = (
f"""Url:\n
{data.link}\n
==========\n
Company:\n
{data.company}\n
==========\n
Title:\n
{data.title}
==========\n
Date:\n
{data.date}
==========\n
Description:\n
{data.description}
==========
"""
    )

    with open(file_name, 'w+') as file:
        file.write(file_content)
    # print('[ON_DATA]', data.title, data.company, data.date, data.link, data.description)


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_executable_path='/Users/karolinaadelbergyte/Desktop/tools/chromedriver', # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=1,  # Slow down the scraper to avoid 'Too many requests (429)' errors
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    # Query(
    #     options=QueryOptions(
    #         optimize=True,  # Blocks requests for resources like images and stylesheet
    #         limit=1  # Limit the number of jobs to scrape
    #     )
    # ),
    Query(
        query='Data Scientist',
        options=QueryOptions(
            locations=['Lithuania'],
            optimize=False,
            limit=100,
            filters=QueryFilters(
                company_jobs_url='https://www.linkedin.com/jobs/search/?f_C=1545609%2C2909062%2C2019%2C24996125%2C5356541%2C3312506%2C14074%2C1273575%2C655894%2C10127&f_E=2%2C3%2C4&geoId=101464403&location=Lithuania',  # Filter by companies
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                type=[TypeFilters.FULL_TIME],
                experience=None,
            )
        )
    ),
]

scraper.run(queries)

