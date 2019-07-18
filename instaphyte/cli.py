#!/usr/bin/env python
import os

import argparse
import requests
import json
from tqdm import tqdm
from socialreaper.tools import save_file, CSV, to_json

from instaphyte.iterators import Instagram

parser = argparse.ArgumentParser(
    description="Scrape Instagram hashtag and location feeds"
)
parser.set_defaults(func=lambda x: parser.print_usage())
parser.add_argument("feed", type=str, choices=["hashtag", "location"],
                    help="The type of feed to scrape posts from")
parser.add_argument("id", type=str,
                    help="The id of the feed to scrape posts from")
parser.add_argument("--count", "-c", type=int, default=0,
                    help="Number for posts to download. 0 to download all")
parser.add_argument("--download", "-d", default=False,
                    action="store_true", help="Save images from posts")
parser.add_argument("--stream", "-s", default=False,
                    action="store_true", help="Stream data into json file")
parser.add_argument("--silent", default=False, action="store_true",
                    help="Disable progress output")
parser.add_argument("--waitDownload", "-w", default=False, action="store_true",
                    help="Only download media once scraping is finished")
parser.add_argument("--filename", "--file", "-f", type=str, default="[id]",
                    help="Name of the output file")
parser.add_argument("--filetype", "--type", "-t", type=str, default="json",
                    choices=["csv", "json", "both"],
                    help="Type of output file")
parser.add_argument("--downdir", type=str,
                    default="downloads/[endpoint]/[id]",
                    help="Directory to save media")


def safe_download(name, url, directory):
    try:
        if not os.path.exists(os.path.join(directory, name)):
            save_file(name, url, directory)
    except requests.exceptions.RequestException:
        print(f"Downloading {url} as {name} to {directory} failed.")
        print("Skipping")


def main():
    args = parser.parse_args()

    api = Instagram()
    if args.silent:
        api.api.log_function = lambda v: None
    function = api.hashtag if args.feed == "hashtag" else api.location
    down_dir = args.downdir \
        .replace("[endpoint]", args.feed) \
        .replace("[id]", args.id)
    filename = args.filename.replace("[id]", args.id)
    
    stream = args.stream and args.filetype != "csv"
    streamFilename = filename + ".json" if args.filetype == "both" or args.filename == "[id]" else ""
    if (stream):
        with open(streamFilename, 'w') as f:
            f.write("[\n")
    
    itr = tqdm(function(args.id, args.count), total=args.count, desc=args.id,
               disable=args.silent)
    posts = []

    for c, post in enumerate(itr):
        if stream:
            with open(streamFilename, 'a') as f:
                if c != 0:
                    f.write(",\n")
                json.dump(post, f, indent=4)
        else:
            posts.append(post)

        if args.download and not args.waitDownload:
            safe_download(post["node"]["shortcode"] + ".jpg",
                          post["node"]["display_url"],
                          down_dir)

    if args.waitDownload and not stream:
        for post in posts:
            safe_download(post["node"]["shortcode"] + ".jpg",
                          post["node"]["display_url"],
                          down_dir)

    if stream:
        with open(streamFilename, "a") as f:
            f.write("]")
        return

    if args.filetype != "json":
        if args.filetype == "both" or args.filename == "[id]":
            filename += ".csv"
        CSV(posts, file_name=filename)

    if args.filetype != "csv":
        if args.filetype == "both" or args.filename == "[id]":
            filename += ".json"
        to_json(posts, filename=filename)


if __name__ == "__main__":
    main()
