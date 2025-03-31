import logging
import os
import sys

from artvee_scraper.artvee_client import CategoryType
from artvee_scraper.artwork import Artwork
from artvee_scraper.scraper import ArtveeScraper



# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] %(module)s.%(funcName)s(%(lineno)d) | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def handle_event(artwork: Artwork, thrown: Exception | None = None) -> None:
    """A callback for handling the result of an artwork processing event."""

    if thrown is not None:
        # An error occurred; the artwork is partially populated (missing artwork.image.raw)
        logger.error("Failed to process artist=%s, title=%s, url=%s; %s", artwork.artist, artwork.title, artwork.url, thrown)
    else:
        file_path = os.path.expanduser(f"~/Downloads/{artwork.resource}.jpg") # create a unique filename
        logger.info("Writing %s to %s", artwork.title, file_path)

        # Write the raw image bytes to a file. 
        with open(file_path, "wb") as fout:
            fout.write(artwork.image.raw)

            
def main():
    # Choose which categories to scrape. Using `list(CategoryType)` creates a list of all categories.
    categories = [CategoryType.DRAWINGS]

    # Initialize the scraper
    scraper = ArtveeScraper(categories=categories)

    # Register listener functions
    scraper.register_listener(handle_event)

    # Start scraping
    with scraper as s:
        s.start() # blocks until done


if __name__ == "__main__":
    main()