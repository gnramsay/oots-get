"""OOTS-Get Archiver.

Create a local archive of the excellent web comic "The Order Of the Stick
(https://www.giantitp.com/comics/oots.html), comic images only.
"""

import os
import re
import shutil
import sys
from pathlib import Path
from typing import Annotated

import requests
import typer
import typer.colors
from bs4 import BeautifulSoup
from rich import print as rprint

from oots_get import __version__

OOTS_URL: str = "https://www.giantitp.com/comics/oots.html"
COMIC_TEMPLATE: str = "https://www.giantitp.com/comics/oots{index}.html"
OUTPUT_DIR: Path = Path(Path.home() / "comics" / "oots")

STATUS_OK = 200
HELP_STRING = "Download the 'Order of the Stick' comics locally."
COPYRIGHT_YEARS = "2013-2024"

app = typer.Typer(rich_markup_mode="rich", add_completion=False)


def get_webpage(page_url: str) -> str:
    """Get the OOTS index webpage and return the content."""
    result = requests.get(page_url, timeout=10)
    if result.status_code == STATUS_OK:
        return result.text

    rprint(
        "Unable to read the OOTS data,please check your connection.",
    )
    rprint("URL : %s", page_url)
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
            rprint(f"[green]Saved {filepath}")
        else:
            rprint("Huh?")
    else:
        rprint(f"[yellow]Skipping {filepath}, already exists.")


def get_last_comic() -> int:
    """Return the index number of the last (highest) comic downloaded."""
    return int(sorted(os.listdir(OUTPUT_DIR), reverse=True)[0].split("-")[0])


@app.command(
    help=HELP_STRING,
    context_settings={"help_option_names": ["-h", "--help"]},
)
def main(
    only_new: Annotated[
        bool,
        typer.Option(
            "--only-new",
            "-n",
            help="Only check for, and download, new comics.",
        ),
    ] = False,
    version: Annotated[
        bool,
        typer.Option(
            "--version", "-v", is_eager=True, help="Show version info"
        ),
    ] = False,
) -> None:
    """Main function to download the comics."""
    if version:
        rprint(
            f"[green]OOTS-get - {HELP_STRING}[/green]"
            f"\nVersion: {__version__} "
            f"\u00a9 {COPYRIGHT_YEARS}\n"
        )
        raise typer.Exit(0)

    rprint(f"oots-get (C) Grant Ramsay 2013-2024 (version {__version__})\n")
    rprint(f"[cyan]Saving Comics to {OUTPUT_DIR}\n")

    check_or_create_folder(OUTPUT_DIR)

    # do specific depending on any command line arguements.
    last_id = get_last_comic() if only_new else 0

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
            rprint("Unable to find image for comic %s", index)
            continue

        image_url = image[0]["src"]
        save_image(image_url, filename)

    rprint("Operation Completed.\n")


if __name__ == "__main__":
    app()
