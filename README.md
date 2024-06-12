# AparatPLD
Aparat Play List Downloader [*]

# Introduction

[Aparat](http://aparat.com) is a `youtube` like site in IRAN hosting lots of videos including some courses from the best universities of IRAN like [Sharif University of Technology](http://sharif.edu).

This script help you to batch download videos playlist.


# Installing dependencies

You can use the `pip` program to install the dependencies on your own.  They are all listed in the `requirements.txt` file.

To use this method, you would proceed as:

```python
pip install -r requirements.txt
```

# Running the script
Run the script to download the materials by providing your desired Aparat play list:

```python
python apld.py "https://www.aparat.com/playlist/954603" --quality 720
```

Finally, the created executable `apd_output.sh` file uses `axel` to download the videos. 

# Courtesy to ...
This code is inspired by [aparatPlayListDownloader](https://github.com/ErfanPY/aparatPlayListDownloader).

[*] The script no longer works because Aparat has changed its pages.
