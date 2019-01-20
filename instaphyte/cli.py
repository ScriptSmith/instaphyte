#!/usr/bin/env python

import argparse
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


def main():
    args = parser.parse_args()

    api = Instagram()
    function = api.hashtag if args.feed == "hashtag" else api.location
    down_dir = args.downdir \
        .replace("[endpoint]", args.feed) \
        .replace("[id]", args.id)

    itr = tqdm(function(args.id, args.count), total=args.count, desc=args.id,
               disable=args.silent)
    posts = []

    for post in itr:
        posts.append(post)
        if args.download and not args.waitDownload:
            save_file(post["node"]["shortcode"] + ".jpg",
                      post["node"]["display_url"],
                      down_dir)

    if args.waitDownload:
        for post in posts:
            save_file(post["node"]["shortcode"] + ".jpg",
                      post["node"]["display_url"],
                      down_dir)

    filename = args.filename.replace("[id]", args.id)

    if args.filetype != "json":
        if args.filetype == "both" or args.filename == "[id]":
            filename += ".csv"
        CSV(posts, file_name=filename)

    if args.filetype != "csv":
        if args.filetype == "both" or args.filename == "[id]":
            filename += ".json"
        to_json(posts, filename=filename)
