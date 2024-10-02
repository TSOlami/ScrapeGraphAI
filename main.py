import json
import nest_asyncio
nest_asyncio.apply()
from scrapegraphai.graphs import SmartScraperGraph
import os
from dotenv import load_dotenv
import time
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
import logging

# Load Environment Variables
load_dotenv()

# Define the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# List of websites to scrape
websites = [
    "https://yconic.com",
    "https://scholarshipscanada.com",
    "https://www.scholarshipca.com/scholarships-in-canada-2025-2026-for-international-students",
    "https://greatyop.com/destination/canada/",
    "https://scholarshipscanada.com/Scholarships/FeaturedScholarships.aspx",
    "https://www.educanada.ca/scholarships-bourses/index.aspx?lang=eng",
    "https://www.scholarships.com/financial-aid/college-scholarships/scholarships-by-state/canada-scholarships/",
    "https://studentawards.com/scholarships/",
    "https://opportunitydesk.org/2024/09/01/canada-scholarships/",
    "https://scholarships360.org/scholarships/study-in-canada-scholarships/",
    "https://scholartree.ca/scholarships/for/international-students"

]

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.FileHandler("scraper.log"),  # Log to a file named scraper.log
        logging.StreamHandler()  # Log to the console
    ]
)

def scrape_site(site, retries=3):
    """Scrape the given site and handle retries if errors occur."""
    for attempt in range(retries):
        try:
            # Log the start of the scraping process for the site
            logging.info(f"Starting scraping process for {site} (Attempt {attempt+1})")

            # Define the configuration for the scraping pipeline
            graph_config = {
                "llm": {
                    "api_key": OPENAI_API_KEY,
                    "model": "openai/gpt-3.5-turbo",
                    "temperature": 0,
                },
                "verbose": True,
                "headless": True,
                "browser_type": "playwright"
            }

            # Create the SmartScraperGraph instance
            smart_scraper_graph = SmartScraperGraph(
                prompt="List me all the master's scholarships available in Canada with their respective Program titles, Managed / Funded by, URLs, deadlines, and requirements.",
                source=site,
                config=graph_config
            )

            # Run the pipeline
            articles_data = smart_scraper_graph.run()

            print("Articles Data:", articles_data)

            # Save the result to a JSON file named after the site
            site_name = site.replace('https://', '').replace('.', '_')
            with open(f'{site_name}_scholarships.json', 'w') as json_file:
                json.dump(articles_data, json_file, indent=4)

            # Log successful scrape
            logging.info(f"Successfully scraped {site}")
            break  # Break out of the retry loop if successful

        except RequestException as e:
            # Log the exception and retry
            logging.error(f"Request error while scraping {site} on attempt {attempt+1}: {e}")
            time.sleep(random.uniform(1, 3))  # Adding delay to avoid IP blocks

        except Exception as e:
            # Log any general exception and stop retries for this site
            logging.error(f"General error occurred while scraping {site}: {e}")
            break

# Use ThreadPoolExecutor to parallelize the scraping process
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(scrape_site, websites)

logging.info("Scraping process completed.")
