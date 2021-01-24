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
    COOKIES = "_ga=GA1.2.177723763.1597843782; auth_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzMzNjM2MTYsImV4cCI6MTYxMjM1ODU4NCwiZXhwX3YyIjoxNjEyMzU4NTg0LCJkZXZpY2UiOiIiLCJ1c2VybmFtZSI6IndlY2hhdF9ha2F0eGdhaiIsImlzX3N0YWZmIjowLCJzZXNzaW9uX2lkIjoiOTcyNmM4NzQ1ZTQ2MTFlYjk5NGJhZTI1ZjljNWE0NzEifQ.D5MUpf567kdEIYICyPN9SqTScl55uMcxm2O1JXxe2Cs; csrftoken=51e68a90e9fabd0c6142d02a7d5fdfe3; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2233363616%22%2C%22first_id%22%3A%221743f4c96153f0-001e216bc91e9e-1d251809-1049088-1743f4c9616323%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22web_codetime%22%2C%22%24latest_utm_medium%22%3A%22shanbay_nav%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%2C%22%24device_id%22%3A%221743f4c96153f0-001e216bc91e9e-1d251809-1049088-1743f4c9616323%22%7D"

    def __init__(self, word: str, savedir="./download", verbose=False):
        os.makedirs(savedir, exist_ok=True)
        self.savedir = savedir
        self.word = word
        self.verbose = verbose
        url = self.API_URL + word
        result = requests.get(url, cookies=cookies2dict(self.COOKIES)).json()
        result = requests.post(
            "http://localhost:1088/decode", json=result).json()
        self.download_url = result["data"]["sound"]

    def download(self):
        if self.verbose:
            print("Downloading {}..".format(self.word))
        urlretrieve(self.download_url["audio_us_urls"][0], os.path.join(
            self.savedir, self.word + ".mp3"))


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
