import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    """
    Fetches image URLs from Google Images for a given search query.

    Parameters:
        query (str): The search term.
        max_links_to_fetch (int): Maximum number of image URLs to fetch.
        wd (webdriver): The Selenium WebDriver instance.
        sleep_between_interactions (int): Sleep time between scrolls.

    Returns:
        set: A set of image URLs.
    """

    def scroll_to_end(wd):
        # Scroll to the bottom of the page to load more images
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # Construct Google Images search URL
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0

    # Loop until we reach the desired number of image URLs
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # Get all image thumbnail elements
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        # Process each thumbnail result to fetch full-size image URL
        for img in thumbnail_results[results_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # Extract image URLs from loaded images
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            # Exit if we have enough images
            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            # If more images are needed, click on the "Load more" button
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)

            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # Update results_start for the next set of thumbnails
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path: str, url: str, counter):
    """
    Downloads and saves an image from a URL.

    Parameters:
        folder_path (str): Folder where image should be saved.
        url (str): URL of the image.
        counter (int): Counter to give the image a unique name.
    """
    image_content = None  # Initialize to avoid referencing before assignment

    try:
        # Request the image content
        image_content = requests.get(url).content
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    # Save the image if content was successfully retrieved
    if image_content:
        try:
            with open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb') as f:
                f.write(image_content)
            print(f"SUCCESS - saved {url} - as {folder_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):
    """
    Searches and downloads images from Google Images.

    Parameters:
        search_term (str): The search term.
        driver_path (str): Path to the ChromeDriver executable.
        target_path (str): Target folder for saving images.
        number_images (int): Number of images to download.
    """
    # Create a folder for the search term if it doesn't exist
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Start Chrome WebDriver with the specified driver path
    service = Service(driver_path)
    with webdriver.Chrome(service=service) as wd:
        # Fetch image URLs
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    # Download each image from the fetched URLs
    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1

# Set up and execute the image search and download
DRIVER_PATH = r'C:\Users\uttka\Downloads\Scraper-20220803T095838Z-001\Scraper\ImageScrapper\ImageScrapper\chromedriver.exe'
search_term = 'Whale'
# specify the number of images to download
search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=150)
