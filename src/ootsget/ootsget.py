"""
OOTS-Get Archiver.

Create a local archive of the excellent web comic "The Order Of the Stick
(https://www.giantitp.com/comics/oots.html), comic images only.
"""

import argparse
import logging
import os
import re
import shutil
import sys

import requests
from bs4 import BeautifulSoup

from ootsget import __version__

OOTS_URL = "https://www.giantitp.com/comics/oots.html"
COMIC_TEMPLATE = "https://www.giantitp.com/comics/oots{index}.html"
OUTPUT_DIR = "~/comics/oots/"

__author__ = "Grant Ramsay"
__copyright__ = "Grant Ramsay"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def get_webpage(page_url):
    """Get the OOTS index webpage and return the content."""
    result = requests.get(page_url)
    if result.status_code == 200:
        return result.text
    else:
        _logger.error(
            "Unable to read the OOTS data,please check your connection."
        )
        _logger.error(f"URL : {page_url}")
        quit(1)


def check_or_create_folder(folder_path):
    """
    Check if the provided folder exists, create if not

    :param folder_path: Path to folder to create.
    :type folder_path: String
    """
    os.makedirs(get_abs_path(folder_path), exist_ok=True)
    return


def get_abs_path(file_path):
    """
    Return an absolute path, expanding '~' and exvironment variables.

    :param file_path: Path to be expanded
    :type file_path: String
    :return: Expanded Path
    :rtype: String
    """
    return os.path.abspath(os.path.expanduser(os.path.expandvars(file_path)))


def save_image(image_url, filename):
    """
    Save the given url to the provided file.

    :param image_url: URL to an image file
    :type image_url: string
    :param filename: Filename to same the file to
    :type filename: string
    """
    extension = image_url[-4:]
    filepath = get_abs_path(OUTPUT_DIR + filename + extension)
    if not os.path.isfile(filepath):
        result = requests.get(image_url, stream=True)
        if result.status_code == 200:
            result.raw.decode_content = True
            with open(filepath, "wb") as f:
                shutil.copyfileobj(result.raw, f)
            print(f"Saved {filepath}")
        else:
            print("Huh?")
    else:
        print(f"Skipping {filepath}, already exists.")


def parse_args(args):
    """
    Parse the Command line parameters.

    :param args: Comand line parameters passed by the user
    :type args: [type]
    :return: A Parser Object
    :rtype: ArguementParser
    """
    parser = argparse.ArgumentParser(
        description="OOTSget (C) Grant Ramsay 2021"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="ootsget {ver}".format(ver=__version__),
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """
    Setup the logging level requested or use default.

    :param loglevel: requested loglevel.
    :type loglevel: [type]
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main(args):
    """
    Run the main function with logging.

    :param args: Command line args passed by user
    :type args: [type]
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting data slurping...")
    print(f"oots-get (C) Grant Ramsay 2021 (version {__version__})\n")
    print(f"Saving Comics to {get_abs_path(OUTPUT_DIR)}\n")
    # get the raw webpage
    webdata = get_webpage(OOTS_URL)
    # parse it with Beautiful Soup
    bs = BeautifulSoup(webdata, "lxml")
    # just get the stuff we want
    links = bs.find_all("p", attrs={"class": "ComicList"})
    # iterate over each link
    for item in reversed(links):
        # create a filename from the title
        index, filename = item.text.split("-", 1)
        # make it 'filename safe'
        filename = filename.strip().replace(" ", "-").replace("/", "-")
        filename = re.sub(r"[?:.#,!'\"]", "", filename)
        # zero pad the index to minimum 4 chars
        index = index.strip().zfill(4)
        # create the final filename
        filename = f"{index}-{filename}"

        # we now get the specific comic page for this item
        comicdata = get_webpage(COMIC_TEMPLATE.format(index=index.strip()))
        # parse it to get the relevant image
        bs = BeautifulSoup(comicdata, "lxml")
        image = bs.find("img", attrs={"src": re.compile("/comics/oots/")})
        image_url = image.get("src")
        # make sure the filder exists, create if not
        check_or_create_folder(OUTPUT_DIR)
        # save that image
        save_image(image_url, filename)

    _logger.info("Script ends here")


def run():
    """Call :func:`main` passing any CLI arguments."""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
