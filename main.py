import json
import nest_asyncio
nest_asyncio.apply()
from scrapegraphai.graphs import SmartScraperGraph

# Load Environment Variables
from dotenv import load_dotenv
load_dotenv()
import os

# Define the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
        "api_key": OPENAI_API_KEY,
        "model": "gpt-3.5-turbo-0125",
        "temperature": 0,
    },
    "verbose": True,
}
# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the masters scholarships available in canada with their respective titles, urls, deadlines and requirements",
    source="<https://ryanocm.substack.com/archive>",
    config=graph_config
)
# Run the pipeline
articles_data = smart_scraper_graph.run()
# Save the result to a JSON file
with open('articles_data.json', 'w') as json_file:
    json.dump(articles_data, json_file, indent=4)