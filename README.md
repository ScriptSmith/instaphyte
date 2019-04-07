# Instaphyte

[![Build Status](https://travis-ci.org/ScriptSmith/instaphyte.svg?branch=master)](https://travis-ci.org/ScriptSmith/instaphyte)
[![Code Quality](https://img.shields.io/codacy/grade/a2322f650025499bb8aee2368ca43207.svg)](https://app.codacy.com/project/ScriptSmith/instaphyte/dashboard)
[![Code Coverage](https://img.shields.io/codacy/coverage/a2322f650025499bb8aee2368ca43207.svg)](https://app.codacy.com/project/ScriptSmith/instaphyte/dashboard)
[![License](https://img.shields.io/github/license/scriptsmith/instaphyte.svg)](https://github.com/ScriptSmith/instaphyte/blob/master/LICENSE)
[![Speed](https://firebasestorage.googleapis.com/v0/b/instagram-speed-test.appspot.com/o/instaphyte.svg?alt=media&token=8e16505d-1259-42a4-90bc-cf8a6d326f55)](https://adamsm.com/instagram-speed-test)

Fast and simple Instagram hashtag and location scraper.

For a more powerful scraper, try [Instamancer](https://github.com/scriptsmith/instamancer)

## Install

### From this repository

```
git clone https://github.com/scriptsmith/instaphyte.git
cd instaphyte
pip3 install -e .
```

### From PIP

```
pip install instaphyte
```

## Usage

### Command Line

```
$ instaphyte
usage: instaphyte [-h] [--count COUNT] [--download] [--silent]
                  [--waitDownload] [--filename FILENAME]
                  [--filetype {csv,json,both}] [--downdir DOWNDIR]
                  {hashtag,location} id

Scrape Instagram hashtag and location feeds

positional arguments:
  {hashtag,location}    The type of feed to scrape posts from
  id                    The id of the feed to scrape posts from

optional arguments:
  -h, --help            show this help message and exit
  --count COUNT, -c COUNT
                        Number for posts to download. 0 to download all
  --download, -d        Save images from posts
  --silent              Disable progress output
  --waitDownload, -w    Only download media once scraping is finished
  --filename FILENAME, --file FILENAME, -f FILENAME
                        Name of the output file
  --filetype {csv,json,both}, --type {csv,json,both}, -t {csv,json,both}
                        Type of output file
  --downdir DOWNDIR     Directory to save media

```


Example:

```
instaphyte hashtag selfie --count=1000 -d
```

### Module

Example:

```python
from instaphyte import Instagram

api = Instagram()

# Get 1000 posts from #selfie
for post in api.hashtag("selfie", 1000):
    print(post)

# Get all posts tagged as being in London
for post in api.location("213385402"):
    print(post)
```
