import os
from urllib.request import urlretrieve

import requests


class ShanBeiWord(object):
    API_URL = "https://www.shanbay.com/api/v1/bdc/search/?version=2&word="

    def __init__(self, word: str, savedir="./download"):
        os.makedirs(savedir, exist_ok=True)
        self.savedir = savedir
        self.word = word
        url = self.API_URL + word
        result = requests.get(url).json()
        self.download_url = result["data"]["audio_addresses"]

    def download(self):
        urlretrieve(self.download_url["us"][0], os.path.join(
            self.savedir, self.word + ".mp3"))


if __name__ == "__main__":
    shanBeiWord = ShanBeiWord("hi")
    shanBeiWord.download()
