
# coding: utf-8

# In[3]:

from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm
import os
import argparse
# Get a copy of the default headers that requests would use
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# In[6]:

def get_args():
    '''This function parses and return arguments passed in'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Script saves images from subreddit')
    # Add arguments
    parser.add_argument(
        '-s', '--subreddit', type=str, help='Subreddit name', required=True)
    parser.add_argument(
        '-n', '--numPages', type=str, help='Number of pages to save from', required=True)
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    subreddit = args.subreddit
    numPages = int(args.numPages)
    # Return all variable values
    return subreddit, numPages

# Run get_args()
# get_args()

# Match return values from get_arguments()
# and assign to their respective variables
subreddit, numPages = get_args()


# In[7]:

url = "https://www.reddit.com/r/"+ subreddit + "/top/?sort=top&t=all"
s = requests.session()
r = s.get(url, headers = headers)
soup = bs(r.text, 'lxml')
extensions = ['png', 'jpg', 'jpeg','ifv2']


# In[ ]:

class subredditTopPostsGenerator:
    def __init__(self, url):
        self.urls = []
        self.baseUrl = url
        r = s.get(url, headers = headers)
        soup = bs(r.text, 'lxml')
        self.urls += [tag['data-url'] for tag in soup.find_all('div', {"data-domain": "i.imgur.com"}) if tag['data-url'][-3:] in extensions]
        self.urls += [tag['data-url'] for tag in soup.find_all('div', {"data-domain":"i.redd.it"})if tag['data-url'][-3:] in extensions]
        self.urls += [tag['data-url'] for tag in soup.find_all('div', {"data-domain":"cdnb.artstation.com"})if tag['data-url'][-3:] in extensions]
        self.nextUrl = soup.find_all('span', {"class":"next-button"})[0].find_all('a')[0]['href']

    def __next__(self):
        temp_r = s.get(self.nextUrl, headers=headers)
        soup = bs(temp_r.text, 'lxml')
        self.urls += [tag['data-url'] for tag in soup.find_all('div', {"data-domain": "i.imgur.com"}) if tag['data-url'][-3:] in extensions]
        self.urls += [tag['data-url'] for tag in soup.find_all('div', {"data-domain":"i.redd.it"})if tag['data-url'][-3:] in extensions]
        self.urls += [tag['data-url'] for tag in soup.find_all('div', {"data-domain":"cdnb.artstation.com"})if tag['data-url'][-3:] in extensions]
        self.nextUrl = soup.find_all('span', {"class":"next-button"})[0].find_all('a')[0]['href']

    def __iter__(self):
        return(self)


# In[ ]:

myurl = 'https://www.reddit.com/r/' + subreddit + "/top/?sort=top&t=all"
myiterator = iter(subredditTopPostsGenerator(myurl))


# In[4]:

def saveUrls(subreddit, urls):
    print("Downloading wallpapers from " "r/" + subreddit)
    
    if not os.path.exists('../figures/'+subreddit):
        os.makedirs('../figures/'+subreddit)

    for i in tqdm(range(len(urls))):
        #print("Downloading..."+subreddit+'/' + tempUrl[7:].replace('/', '_').strip('_'))
        tempUrl = urls[i]
        r = s.get(tempUrl, headers=headers, stream=True)
        
        if not os.path.exists('../figures/'+subreddit +'/'+ tempUrl[7:].replace('/', '_').strip('_') ):
            with open('../figures/'+subreddit +'/'+ tempUrl[7:].replace('/', '_').strip('_') , 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
        else:
            continue


# In[5]:

for i in range(numPages):
    next(myiterator)
#print(myiterator.urls)


# In[6]:

saveUrls(subreddit, myiterator.urls)


# In[ ]:




# In[ ]:



