# Panopto Downloader

Tool created after a fork from https://github.com/karim-selih/Panopto-Downloader.

## Installation
### Requirements
```
pip install -r requirements.txt
```

## Usage

On first run, run 

```
python3 get_cookies.py --url "https://scs.hosted.panopto.com"
```
Now, authenticate with panopto, and press enter on the terminal. If using DUO, ensure that you clikc this is my device. This will save auth cookies.


Now, change the variables correctly in `download_course.sh`. 
- Baseurl is the base link of the panopto subdomain for your institute.
- Tableurl is the tabular view of the folder of videos that you wish to download. Ensure that you have all of the videos in the same table (change max videos to 150)

Run 
```
./download_course.sh
```

This will download all videos!