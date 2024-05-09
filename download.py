from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from ffmpeg_progress_yield import FfmpegProgress
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import time
import json
import os
import argparse
from pathlib import Path
import wget
import pickle

import requests


class panoptoDownloader:
    def __init__(self, base_url: str, courseid: str, table_url : str):
        self.BASE_URL = base_url
        self.table_url = table_url
        self.s = requests.Session()
        self.directory = 'downloads/' + courseid
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

    def get_visible_videos(self, driver: WebDriver) -> list[str]:
        soup = BeautifulSoup(str(driver.page_source), "html.parser")
        a_s = soup.find_all("a", attrs={"class": "list-title"})
        final_videos = []
        i = 0
        for a in a_s:
            if a is not None:
                if 'href' in a.attrs:
                    print(a['href'], a.text)
                    final_videos.append([a['href'], a.text])

        with open(f"{self.directory}/vidoes.json", "w") as f:
            json.dump(final_videos, f)
        return final_videos


    def run(self,):

        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

        driver.get(self.BASE_URL)
        if os.path.exists("cookies.pkl"):
            print("Loading cookies")
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)

        driver.get(self.table_url)
        time.sleep(2)
        
        videos = self.get_visible_videos(driver)

        for i in range(len(videos)):
            link = videos[i][0]
            driver.get(link)
            time.sleep(2)
            soup = BeautifulSoup(str(driver.page_source), "html.parser")
            
            a_s = soup.find_all("video", attrs={"id": "primaryVideo", "class":"video-js"})
            
            for a in a_s:
                if a is not None:
                    if 'src' in a.attrs:
                        print(a['src'], a.text)
                        videos[i][0] = a['src']

        with open(f"{self.directory}/videos.json", "w") as f:
            json.dump(videos, f)
        


        print("Downloading videos...")        
        task_id = 0

        for i, video in enumerate(videos):
            video_name = f"Lecture{len(videos) - i}"
            out = "out/{}.mp4".format(video_name)
            print(f"Downloading {video_name}")
            wget.download(link, out=out)
            task_id += 1

        print("Completed!")

        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="-Panopto Downloader-")
    parser.add_argument(
        "--baseurl", metavar="url", type=str, help="[REQ] panopto url", required=True
    )
    parser.add_argument(
        '--courseid', metavar='courseid', type=str, help='course id', required=True
    )
    parser.add_argument(
        '--tableurl', metavar='courseid', type=str, help='course id', required=True
    )
    
    args = parser.parse_args()

    dl = panoptoDownloader(args.baseurl, args.courseid, args.tableurl)
    dl.run()
