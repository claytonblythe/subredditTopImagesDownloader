from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import os
import argparse

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


class SubbredditTopPostsGenerator:
    def __init__(self, base_url, subreddit):
        self.image_urls = []
        self.baseUrl = base_url
        self.session = requests.session()
        self.extensions = ['png', 'jpg', 'jpeg', 'ifv2']
        self.domains = ["i.imgur.com", "i.redd.it", "cdnb.artstation.com"]
        self.subreddit = subreddit
        self.first_iter = True
        self.next_url = base_url

    def __next__(self):
        r = self.session.get(self.next_url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        self.image_urls += [tag['data-url'] for domain in self.domains for tag in
                      soup.find_all('div', {"data-domain": domain}) if
                      tag['data-url'][-3:] in self.extensions]
        self.next_url = soup.find_all('span', {"class": "next-button"})[0].find_all('a')[0]['href']

    def __iter__(self):
        return self

    def save_urls(self):
        if not os.path.exists('../figures/' + subreddit + '/' + timeframe):
            os.makedirs('../figures/' + subreddit + '/' + timeframe)

        for idx in tqdm(range(len(self.image_urls))):
            this_image_url = self.image_urls[idx]

            if not os.path.exists(
                    '../figures/' + subreddit + '/' + timeframe + '/' + this_image_url[7:].replace('/', '_').strip('_')):
                r = self.session.get(this_image_url, headers=headers, stream=True)
                with open('../figures/' + subreddit + '/' + timeframe + '/' + this_image_url[7:].replace('/', '_').strip('_'),
                          'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
            else:
                continue


def get_args():
    """This function parses and return arguments passed in"""
    parser = argparse.ArgumentParser(
        description='Script saves images from subreddit')
    parser.add_argument(
        '-s', '--subreddit', type=str, help='Subreddit name', default='EarthPorn')
    parser.add_argument(
        '-n', '--num_pages', type=int, help='Number of pages to save from', default=1)
    parser.add_argument(
        '-t', '--timeframe', type=str, help='Time frame to save from', default='all')
    args = parser.parse_args()
    subreddit = args.subreddit
    num_pages = args.num_pages
    timeframe = args.timeframe
    return subreddit, num_pages, timeframe


if __name__ == "__main__":
    subreddit, num_pages, timeframe = get_args()
    base_url = f"https://old.reddit.com/r/{subreddit}/top/?sort=top&t={timeframe}"
    my_iterator = iter(SubbredditTopPostsGenerator(base_url, subreddit))
    for _ in range(num_pages):
        next(my_iterator)

    my_iterator.save_urls()
