#!/usr/bin/env python3
import io, sys, os
import argparse
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from rich.progress import track
from rich import print
import re

def usage():
    return f"""
        {sys.argv[0]} "Link" [-q quality]
        python {sys.argv[0]} "https://www.aparat.com/playlist/954603" [-q 720]
        The default quality is 720.
    """

def main():
    print("Please wait ...")
    session = HTMLSession()
    r = session.get(link)
    r.html.render()
    main_soup = bs(r.html.html, 'html.parser')
    course = main_soup.find('div', attrs={'class':'playlist-field'}).find('h1').find('span').text
    playlist = main_soup.find_all('a', attrs={'class':'titled-link title'})
    video_pages = [f"https://www.aparat.com{re.findall('/./.*?/', l.attrs['href'])[0]}" for l in playlist]
    count=len(video_pages)
    print(f"This playlist contains {count} videos [green][{course}][/green]")
    links = {}
    script = """//https://github.com/psf/requests-html/issues/355
        () => {
            setTimeout(function(){
                document.querySelector('[aria-label="download"]').click();
            }, 3000);
        }
    """
    for page in track(video_pages, description="Downloading the video URLs ..."):
        r = session.get(page)
        r.html.render(script=script, sleep=5)
        soup = bs(r.html.html, 'html.parser')
        name = soup.find("title").text
        print(f"[blue]{name}[/blue]")
        qualities = [_ for _ in [soup.find('a', attrs={'id':f'{_}'})
            for _ in ('144p', '240p', '360p', '480p', '720p', '1080p') ] if _]
        for qual in qualities:
            if quality in qual.get('id'):
                links[name] = qual.get('href')
                break
        else:
            links[name] = qual.get('href')
    print("Writing download list ...")
    with io.open(os.open('apd_output.sh', os.O_CREAT | os.O_WRONLY, 0o777), "w", encoding="utf-8") as file:
        file.write(f"#!/bin/bash\n")
        for i, (name, videoLink) in enumerate(links.items(), 1):
            file.write(f"axel {videoLink} -o \"{i:02d}_{name}.mp4\"\n")
    print('Playlist Made! Just run [red]./apd_output.sh[/red] in your terminal.')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Aparat Playlist Downloader(APD)", usage=usage())
    parser.add_argument("link", help="main page Link")
    parser.add_argument("-q", "--quality", help="eg: [144, 240, 360, 480, 720, 1080]", default='720')

    args = parser.parse_args()
    link = args.link
    quality = args.quality

    main()