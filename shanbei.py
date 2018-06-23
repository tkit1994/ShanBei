import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlretrieve

import requests
from tqdm import tqdm


class ShanBeiWord(object):
    API_URL = "https://www.shanbay.com/api/v1/bdc/search/?version=2&word="

    def __init__(self, word: str, savedir="./download", verbose=False):
        os.makedirs(savedir, exist_ok=True)
        self.savedir = savedir
        self.word = word
        self.verbose = verbose
        url = self.API_URL + word
        result = requests.get(url).json()
        self.download_url = result["data"]["audio_addresses"]

    def download(self):
        if self.verbose:
            print("Downloading {}..".format(self.word))
        urlretrieve(self.download_url["us"][0], os.path.join(
            self.savedir, self.word + ".mp3"))


def work(word):
    if word:
        shanBeiWord = ShanBeiWord(word, verbose=False)
        shanBeiWord.download()


if __name__ == "__main__":

    with open("word.txt", 'r') as f:
        word_list = f.read().splitlines()
    with ThreadPoolExecutor(5) as executor:
        future_list = [executor.submit(work, word) for word in word_list]
        for future in tqdm(as_completed(future_list), total=len(word_list), ascii=True):
            pass
