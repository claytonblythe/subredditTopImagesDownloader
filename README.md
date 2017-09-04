# Subreddit Top Image Downloader

This is a project called subredditTopImagesDownloader created by Clayton Blythe on 2017/07/19 

Email: blythec1@central.edu

Here is an example of a top post from the r/wallpaper subreddit that is downloaded to the figure directory

![Alt Test](https://github.com/claytonblythe/subredditTopImagesDownloader/blob/figures/figures/MinimalWallpaper/all/i.imgur.com_vTMGurl.png)

![Alt Test](https://github.com/claytonblythe/subredditTopImagesDownloader/blob/figures/figures/wallpaper/all/i.imgur.com_IB8Sjzt.png)

## Methods

Here I employ the BeautifulSoup library in python to experiment with object oriented programming and generators for building a list of imgur or 
other readily available image links of popular image posts from a particular subreddit. I use BeautifulSoup to scrape the relevant image links for a 
specified number of pages from the most voted pages for that subreddit. I use classes and tqdm to provide a progress bar that allows the user to see
how much estimated time is remaining for downloading the images. The script tests if the files and/or directories exist and creates them if they do not. Additionally, 
the script checks if the file already exists before downloading. 

I think I could improve my error handling, to incorporate try and except clauses, and maybe work on organizing my object initialization. Regardless, it works currently at a pretty impressive and fast rate, 
allowing one to easily download the top most popular images from a subreddit over a given timeframe. 
 

## Requirements

Here I am using Python 3.6, with the modules bs4, requests, os, argparse, and tqdm imported. 


## Usage

To use this utility: 

1. Type "git clone --depth=1 https://github.com/claytonblythe/subredditTopImagesDownloader.git" in a directory where you want this repository to reside
2. Type "cd subredditTopImagesDownloader/code" to navigate into the directory with the script
3. Type "python subredditTopImagesDownloaderGenerator.py" to run the script, which will by default download the images from the top page of all-time most 
upvoted posts on r/EarthPorn 

If you wish to download from a specific subreddit, over a range of pages, and over a specified time you can specify this with command line arguments of -s, -n, and -t respectively. Below is an example of how you can use this functionality to download all the images from the first three pages of the r/wallpaper subreddit's historical most-upvoted posts. 

![Alt Test](https://asciinema.org/a/vZ7wnHS7UCljSW8V4vDWYh747)

Overall I am very satisfied with the result. I am still learning Python so I am open to any suggestions anyone has to improve performance and/or write better code. 

Hope you find this useful. 
