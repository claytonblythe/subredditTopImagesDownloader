import argparse
import asyncio
import os
import os.path
import time

import aiofiles as aiofiles
import aiohttp as aiohttp
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


class SubbredditTopPostsGenerator:
    def __init__(self, base_url, subreddit):
        self.image_urls = []
        self.baseUrl = base_url
        self.session = requests.session()
        self.async_loop = asyncio.get_event_loop()
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

    async def fetch(self, session, url):
        try:
            async with session.get(url, timeout=None, ssl=False) as response:
                if response.status != 200:
                    response.raise_for_status()
                else:
                    filepath = '../figures/' + self.subreddit + '/' + timeframe + '/' + url[7:].replace('/', '_').strip(
                        '_')
                    buffer = b""
                    if not os.path.exists(os.path.dirname(filepath)):
                        await os.makedirs(os.path.dirname(filepath))
                    if not os.path.exists(filepath):
                        f = await aiofiles.open(filepath, mode='wb')
                        async for chunk in response.content.iter_any():
                            buffer += chunk
                        await f.write(buffer)
                        await f.close()
        except Exception as e:
            print(e)

    async def fetch_all(self):
        async with aiohttp.ClientSession(loop=self.async_loop) as session:
            results = await asyncio.gather(*[self.async_loop.create_task(self.fetch(session, url))
                                             for url in self.image_urls])
        return results


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
    return subreddit,  num_pages, timeframe


if __name__ == "__main__":
    before = time.time()
    subreddit, num_pages, timeframe = get_args()
    base_url = f"https://old.reddit.com/r/{subreddit}/top/?sort=top&t={timeframe}"
    my_iterator = SubbredditTopPostsGenerator(base_url, subreddit)
    for _ in range(num_pages):
        next(my_iterator)

    my_iterator.async_loop.run_until_complete(my_iterator.fetch_all())
    print(f"{len(my_iterator.image_urls)} urls in {time.time()-before} seconds")
    print(len(set(my_iterator.image_urls)))
