#!/usr/bin/python
import io, sys
import argparse
import requests as req
from bs4 import BeautifulSoup as bs
from rich.progress import track

def usage():
    return f"""
        {sys.argv[0]} "Link" [-q quality]
        python {sys.argv[0]} "https://www.aparat.com/playlist/954603" [-q 720]
        The default quality is 720.
    """

def main():
    print("Please wait...")
    mainPage = req.get(link).content
    main_soup = bs(mainPage, 'html.parser')
    main_name = main_soup.find_all("div", attrs={"class":"content pl-sm"})
    
    playlist = main_soup.find_all('h2', attrs={'class':'title'})
    playListLinks = []
    for i,item in enumerate(playlist):
        playListLinks.append(item.find('a'))
    
    video_pages = [f"https://www.aparat.com{video.get('href')}" for video in playListLinks]
    count=len(video_pages)
    print(f"This playlist contains {count} videos")
    
    links = {}
    for index,page in enumerate(track(video_pages, description="Downloading the video URLs ...")) :
        html = req.get(page).content
        soup = bs(html, 'html.parser')
        name = soup.find("h1", attrs={"id":"videoTitle", "class":"title"}).text.encode()
        qualitys = soup.find('div', attrs={'class':'dropdown-content'}).find_all('a')
        for qual in qualitys :
            if quality in qual.get('aria-label'):
                links[name] = qual.get('href')
            elif "720" in qual.get('aria-label'):
                links[name] = qual.get('href')
    print("Writing download list ...")
    
    with io.open('apd_output.sh', "w", encoding="utf-8") as file:
        file.write(f"#!/bin/bash\n")
        for i, (name, videoLink) in enumerate(links.items(), 1):
            file.write(f"axel {videoLink} -o \"{i:02d}_{name.decode('utf-8')}.mp4\"\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Aparat Playlist Downloader(APD)", usage=usage())
    parser.add_argument("link", help="main page Link")
    parser.add_argument("-q", "--quality", help="eg: [124, 360, 480, 720, 1080]", default='720')

    args = parser.parse_args()
    link = args.link
    quality = args.quality

    main()