from http.client import SEE_OTHER
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict
from urllib.request import urlretrieve
import argparse
import requests
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(
        "A script to download word audio from ShanBei")
    parser.add_argument(
        "-v", "--verbose", help="weather to verbose downloading words", action="store_true")
    parser.add_argument(
        "-f", "--file", type=str, help="input file to download", default='./word.txt')
    parser.add_argument(
        "-s", "--save_dir", type=str, help="output directory", default="./download")
    parser.add_argument(
        "-t", "--threads", type=int, help="number of threads to use for downloading", default=5)
    return parser.parse_args()


def cookies2dict(cookies: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for line in cookies.split(";"):
        if line.find("=") != -1:
            name, value = line.strip().split("=")
            result[name] = value
    return result


class ShanBeiWord(object):
    API_URL = "https://apiv3.shanbay.com/wordsapp/words/vocab?word="

    def __init__(self, word: str, savedir="./download", verbose=False):
        os.makedirs(savedir, exist_ok=True)
        self.savedir = savedir
        self.word = word
        self.verbose = verbose
        url = self.API_URL + word
        result = requests.get(url, cookies=cookies2dict(
            os.getenv("COOKIES"))).json()
        result = requests.post(
            "http://localhost:1088/decode", json=result).json()
        self.audio_urls = result["data"]["sound"]

    @property
    def download_url(self):
        return self.audio_urls["audio_us_urls"][0]

    @property
    def audio_ext(self):
        return os.path.splitext(self.download_url)[1]

    def download(self):
        if self.verbose:
            print("Downloading {}..".format(self.word))
        urlretrieve(self.download_url, os.path.join(
            self.savedir, self.word + self.audio_ext))


def work(word):
    if word:
        shanBeiWord = ShanBeiWord(
            word, verbose=args.verbose, savedir=args.save_dir)
        shanBeiWord.download()


if __name__ == "__main__":
    args = parse_args()

    with open(args.file, 'r') as f:
        word_list = f.read().splitlines()
    with ThreadPoolExecutor(args.threads) as executor:
        future_list = [executor.submit(work, word) for word in word_list]
        for future in tqdm(as_completed(future_list), total=len(word_list), ascii=True):
            pass
