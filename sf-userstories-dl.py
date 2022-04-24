import requests, json, argparse, logging
import http.cookiejar as cookielib
from bs4 import BeautifulSoup, Tag
from typing import List, cast
from collections import namedtuple
from pathlib import Path

Folder = namedtuple('Folder', ['title', 'url'])
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(
    description="Download all story metadata from any author on SoFurry")
parser.add_argument("-c", "--cookies", help="cookies.txt file to login to SoFurry")
parser.add_argument("-o", "--output", help="Json file to write with story info.", 
    default="stories.json", type=argparse.FileType("w"))
parser.add_argument("--agent", help="Downloader user agent.", 
    default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
parser.add_argument("username", help="The SoFurry author to download.")

args = parser.parse_args()

session = requests.session()
session.headers.update({'User-Agent': args.agent})

# Load cookies from a netscape cookie file (if provided)
if args.cookies:
    cookies = cookielib.MozillaCookieJar(args.cookies)
    cookies.load()
    session.cookies = cookies #type:ignore 


def getUserId(username: str):
    resp = session.get("http://api2.sofurry.com/std/getUserProfile", params={"username": username})
    return resp.json()["userID"]

def getFolders(uid: str):
    resp = session.get("https://api2.sofurry.com/browse/user/stories", params={"uid": uid})
    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.find_all("a")


    # find all links
    folders = [Folder(x['title'], x['href']) for x in cast(List[Tag], links) if "href" in x.attrs and "&folder=" in x["href"] and "title" in x.attrs]
    return folders

def getStoriesNotInFolder(uid: str):
    user_stories_url = "https://api2.sofurry.com/browse/user/stories"
    first_story_urls = set()
    stories = []

    page = 1

    while True:
        resp = session.get(user_stories_url, params={"stories-page": page, "format": "json", "uid": uid})
        s = resp.json()["items"]

        if s[0]["link"] in first_story_urls: return stories # repeat page

        first_story_urls.add(s[0]["link"])
        stories.extend(s)
        page += 1


def getStoriesInFolder(folder_url: str):
    folder_url = "https://api2.sofurry.com" + folder_url #this already has the base parameters
    first_story_urls = set()
    stories = []

    page = 1

    while True:
        resp = session.get(folder_url, params={"stories-page": page, "format": "json"})
        s = resp.json()["items"]

        if s[0]["link"] in first_story_urls: return stories # repeat page

        first_story_urls.add(s[0]["link"])
        stories.extend(s)
        page += 1


if __name__=='__main__':
    uid = getUserId(args.username)

    logging.info(f"Username {args.username} is SoFurry uid: {uid}")

    folders = getFolders(uid)
    logging.info(f"Found {len(folders)} story folders for {args.username}")

    stories = []

    logging.info("Fetching data for all stories not in a folder.")
    stories.extend([{**x, 'folder': None} for x in getStoriesNotInFolder(uid)])
    
    for f in folders:
        logging.info(f"Fetching data for stories in folder: {f.title}")
        stories.extend([{**x, 'folder': f.title} for x in getStoriesInFolder(f.url)])

    # adjust story links to refer to the common SF URLs not the API urls.
    stories = [{**x, 'link': x['link'].replace("api2.sofurry.com", "sofurry.com")} for x in stories]

    json.dump(stories, args.output, indent=2)
    logging.info(f"Wrote {len(stories)} to {args.output.name}")