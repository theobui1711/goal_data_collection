import argparse

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# import re

import pandas as pd

from helper.config import GOOGLE_SEARCH_URL


class Crawler:
    def __init__(self, query, number_of_pages):
        self.url = GOOGLE_SEARCH_URL
        self.query = query
        self.number_of_pages = number_of_pages
        self.driver = self.init_driver()

    @staticmethod
    def init_driver():
        # init web driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        return driver

    def get_snippets(self, searching_url):
        snippets = []
        self.driver.get(searching_url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        raw_data = soup.find_all("div", {"class": "VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"})
        for i in raw_data:
            time = i.find("span", {"class": "MUxGbd wuQ4Ob WZ8Tjf"})
            if time:
                time.string = time.text.replace(time.text, "")
            i.prettify()
            snippets.append(i.text)
        return snippets

    def get_goal_sentences(self, snippets):
        results = []
        for snippet in snippets:

            # process with ""
            snippet = snippet.replace('"', ' ').replace(':', ".")

            for sentence in snippet.split("."):
                # sentence = re.sub(r'[^\w\s]', '', sentence)
                sentence = sentence.strip()
                if self.query.lower() in sentence.lower() \
                        and len(sentence) > len(self.query) \
                        and "my" in sentence.lower()[:5]:
                    sentence += "."
                    if sentence not in results:
                        results.append(sentence)
        return results

    def save_csv_file(self, goal_sentences):
        # pandas loads data
        dict_results = []
        for sentence in goal_sentences:
            dict_results.append(
                {
                    "Trigger phrase": self.query,
                    "Goal": sentence[len(self.query) + 1:].strip()
                }
            )
        df = pd.DataFrame(dict_results)
        print(df)

        # save file
        file_name = "_".join(self.query.lower().split(" "))
        df.to_csv("data/" + file_name, sep='\t', encoding='utf-8', index=False)

    def run(self):
        results = []
        for page in range(1, self.number_of_pages + 1):
            searching_url = self.url + self.query + "&start=" + str((page - 1) * 10)
            snippets = self.get_snippets(searching_url)
            goal_sentences = self.get_goal_sentences(snippets)
            for sentence in goal_sentences:
                if sentence not in results:
                    results.append(sentence)
        self.save_csv_file(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Goal data collection")
    parser.add_argument("-tp", "--trigger_phrase", type=str,
                        help="The trigger phrase to use for web scraping",
                        default="My goal is to", required=True)
    parser.add_argument("-n", "--number", type=int,
                        help="The number of results to collect",
                        default=10, required=True)
    args = vars(parser.parse_args())
    trigger_phrase = args["trigger_phrase"]
    page_number = args["number"]
    crawler = Crawler(trigger_phrase, page_number)
    crawler.run()
