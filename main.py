import time
from instagrapi import Client
import requests
from moviepy.editor import VideoFileClip


class TIbot:

    def __init__(self, username: str, password: str, sleep: int, tiktok_usernames: list) -> None:

        self.username = username
        self.password = password
        self.sleep = sleep
        self.tiktok_usernames = tiktok_usernames
        self.video_ids = []
        self.cl = Client()
        if self.cl.login(self.username, self.password):
            print("Login sucscessful")

    def video_download(self, url: str, filename: str) -> None:

        chunk_size = 256
        r = requests.get(url, stream=True)
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)

    def video_uploadO(self, filename: str) -> None:

        self.cl.clip_upload(filename, caption="TEST")

    def get_last_video_id_form_tiktok(self, tiktokusername: str) -> str:

        response = requests.get(
            "https://api-v1.majhcc.com/api/tk/getlastvideoid?username={}".format(tiktokusername))

        return response.json()["download_url"], response.json()["video_id"]

    def run(self) -> None:

        while True:

            for tiktokusername in self.tiktok_usernames:
                video_url, video_id = self.get_last_video_id_form_tiktok(
                    tiktokusername)
                if video_id in self.video_ids:

                    print("No new video found")
                    continue

                else:

                    self.video_download(video_url, "video.mp4")
                    clip = VideoFileClip("video.mp4")
                    duration = clip.duration

                    if duration > 60:
                        print("Video is too long")
                        continue

                    else:

                        try:

                            self.video_uploadO("video.mp4")
                            print("{} uploaded {}".format(
                                tiktokusername, video_id))
                            self.video_ids.append(video_id)
                        except:

                            print("Upload failed")
                            continue

            print("Sleeping for {} minutes".format(self.sleep))
            time.sleep(self.sleep * 60)


TIbot("username", "password", 1, ["majhc", "tiktok", "asdf"]).run()
