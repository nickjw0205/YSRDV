import pandas as pd
from io import BytesIO
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pytube import YouTube # => to download video from youtube
from pytube.cli import on_progress
import time
import cv2
import sys
import numpy as np
import torch
from urllib import request
from PIL import Image
from tqdm import tqdm


# video title and link list
titles = []
links = []
# basic links for code
basic_link = 'https://www.youtube.com'
basic_search_link = 'https://www.youtube.com/results?search_query='
comons_url = "&sp=EgIwAQ%253D%253D"

def search_youtube(search, args):
    path = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path)
    delay = 3
    driver.implicitly_wait(delay)
    driver.get(search)
    # body = driver.find_element_by_tag_name('body')
    body = driver.find_element(By.TAG_NAME, 'body')
    num_of_pagedowns = args.scroll
    while num_of_pagedowns >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        num_of_pagedowns -= 1
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
    return soup

# add video title and link to list
def search_titles(soup):
    # print(soup.select('style-scope yt-img-shadow')[0])
    for a in soup.find_all('a','yt-simple-endpoint style-scope ytd-video-renderer'):
        links.append(basic_link+a['href'])
    return links

def search_word(input_word, args):
    word = input_word.replace(" ", "+")
    if args.cc_license:
        search_link = basic_search_link+word+comons_url
    else:
        search_link = basic_search_link+word

    return search_link

def write_link_to_csv(data_list, links, args):
    # original_columns = ['link', 'status', 'author', 'videoId', 'channel_id', 'title', 'length', 'width', 'height','fps', 'captured_status', 'slide_#', 'non_slide_#', 'total_#']

    download_list = []
    downloaded_list = []
    
    for index, row in data_list.iterrows():
        downloaded_list.append(row['Link'])
    
    for link in links:
        if link not in downloaded_list:
            data_list = data_list.append({'Link': link, 'status': "X", 'author':"-", 'videoId':"-", 'channel_id':"-",
                                          'title':"-", 'length':"-", 'width':"-", 'height':"-",'fps':"-"}, ignore_index=True)
            download_list.append(link)
    data_list.to_csv(args.csv_path, mode='w', index=False)
            
    print("{0} links are added to csv".format(len(download_list)))
    return data_list

def get_search_list(data_list, args):
    links = search_titles(search_youtube(search_word(args.keyword, args), args))
    write_link_to_csv(data_list, links, args)
    return data_list