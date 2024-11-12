### Google Image Scraper
This project is a Python-based web scraper that uses Selenium to search and download images from Google Images based on a given search term. The project automates the process of scrolling through Google Images results, clicking on image thumbnails to load full-size images, and saving the images to a local directory.

Features
Automated Image Search: Uses Selenium WebDriver to perform Google Images searches.
Scroll to Load More Images: Automatically scrolls to the end of the page to load more images, simulating user behavior.
Thumbnail Click and Full-size Image Extraction: Clicks on each image thumbnail to load and retrieve the full-size image URL.
Image Download and Storage: Downloads the images and saves them in a specified directory with unique filenames.
Prerequisites
Before running this project, ensure you have the following installed:

Python (version 3.6 or higher)
Google Chrome: Required for Selenium to run Chrome in headless mode.
ChromeDriver: The version of ChromeDriver should match your installed version of Chrome.
