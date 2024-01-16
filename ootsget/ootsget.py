"""OOTS-Get Archiver.

Create a local archive of the excellent web comic "The Order Of the Stick
(https://www.giantitp.com/comics/oots.html), comic images only.
"""

import argparse
import contextlib
import logging
import os
import re
import shutil
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from rich import print  # pylint: disable=W0622

from ootsget import __version__

OOTS_URL: str = "https://www.giantitp.com/comics/oots.html"
COMIC_TEMPLATE: str = "https://www.giantitp.com/comics/oots{index}.html"
OUTPUT_DIR: Path = Path(Path.home() / "comics" / "oots")

STATUS_OK = 200

__author__ = "Grant Ramsay"
__copyright__ = "Grant Ramsay"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def get_webpage(page_url: str) -> str:
    """Get the OOTS index webpage and return the content."""
    result = requests.get(page_url, timeout=10)
    if result.status_code == STATUS_OK:
        return result.text

    _logger.error(
        "Unable to read the OOTS data,please check your connection.",
    )
    _logger.error("URL : %s", page_url)
    sys.exit(1)


def check_or_create_folder(folder_path: Path) -> None:
    """Check if the provided folder exists, and create if not.

    :param folder_path: Path to folder to create.
    :type folder_path: String
    """
    folder_path.mkdir(parents=True, exist_ok=True)


def save_image(image_url: str, filename: str) -> None:
    """Save the given url to the provided file.

    :param image_url: URL to an image file
    :type image_url: string
    :param filename: Filename to same the file to
    :type filename: string
    """
    extension = image_url[-4:]
    filepath = OUTPUT_DIR / (filename + extension)
    if not filepath.is_file():
        result = requests.get(image_url, stream=True, timeout=20)
        if result.status_code == STATUS_OK:
            result.raw.decode_content = True
            with filepath.open(mode="wb") as f:
                shutil.copyfileobj(result.raw, f)
            print(f"[green]Saved {filepath}")
        else:
            print("Huh?")
    else:
        print(f"[yellow]Skipping {filepath}, already exists.")


def parse_args(args: list[str]) -> argparse.Namespace:
    """Parse the Command line parameters.

    :param args: Comand line parameters passed by the user
    :type args: [type]
    :return: A Parser Object
    :rtype: ArguementParser
    """
    parser = argparse.ArgumentParser(
        description=f"oots-get (C) Grant Ramsay 2022 (Version {__version__})"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ootsget {__version__}",
    )

    parser.add_argument(
        "--only-new",
        "-n",
        action="store_true",
        help="Only check for, and download, new comics.",
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


def setup_logging(loglevel: int) -> None:
    """Setup the logging level requested or use default.

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


def get_last_comic() -> int:
    """Return the index number of the last (highest) comic downloaded."""
    return int(sorted(os.listdir(OUTPUT_DIR), reverse=True)[0].split("-")[0])


def main(raw_args: list[str]) -> None:
    """Run the main function with logging.

    :param args: Command line args passed by user
    :type args: [type]
    """
    args = parse_args(raw_args)
    setup_logging(args.loglevel)

    _logger.debug("Starting data slurping...")
    print(f"oots-get (C) Grant Ramsay 2024 (version {__version__})\n")
    print(f"[cyan]Saving Comics to {OUTPUT_DIR}\n")

    check_or_create_folder(OUTPUT_DIR)

    # do specific depending on any command line arguements.
    last_id = get_last_comic() if args.only_new else 0

    # get the comic index webpage and parse the links
    webdata = get_webpage(OOTS_URL)
    bs = BeautifulSoup(webdata, "lxml")
    links = bs.find_all("p", attrs={"class": "ComicList"})
    for item in links:
        index, filename = item.text.split("-", 1)
        index = index.strip().zfill(4)

        # break here if we are only getting new comics
        if last_id >= int(index):
            break

        filename = filename.strip().replace(" ", "-").replace("/", "-")
        filename = re.sub(r"[?:.#,!'\"]", "", filename)
        filename = f"{index}-{filename}"

        # we now get the specific comic for this item
        comicdata = get_webpage(COMIC_TEMPLATE.format(index=index.strip()))
        bs = BeautifulSoup(comicdata, "lxml")
        image = bs.find_all("img", attrs={"src": re.compile("/comics/oots/")})

        if len(image) == 0:
            _logger.error("Unable to find image for comic %s", index)
            continue

        image_url = image[0]["src"]
        save_image(image_url, filename)

    print("Operation Completed.\n")
    _logger.info("Script ends here")


def run() -> None:
    """Call :func:`main` passing any CLI arguments."""
    with contextlib.suppress(KeyboardInterrupt):
        main(sys.argv[1:])


if __name__ == "__main__":
    run()
