from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import pickle

       


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="-Panopto Downloader-")
    parser.add_argument(
        "--url", metavar="url", type=str, help="[REQ] panopto url", required=True
    )
    args = parser.parse_args()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get(args.url)
    input("Login, and then press any key here. ")
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    driver.quit()