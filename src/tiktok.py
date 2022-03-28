from playwright.sync_api import sync_playwright
import requests
import re


def get_last_video_url(username):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        browser = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36")
        page = browser.new_page()
        page.goto("http://tiktok.com/@{}".format(username))
        latest_video = page.query_selector(
            'xpath=/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/a')
        url = latest_video.get_property('href')
        browser.close()
        return url


def get_download_url(username):
    url = get_last_video_url(username)
    url = str(url) + '/'
    video_id = re.findall(
        r'https\:\/\/www\.tiktok\.com\/@majhc\/video\/(.*?)\/', url)[0]
    resopnses = requests.get(
        'https://api-v1.majhcc.com/api/tk?url={}'.format(url))
    return resopnses.json()['link'], video_id
