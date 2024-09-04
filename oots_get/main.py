"""OOTS-Get Archiver.

Create a local archive of the excellent web comic "The Order Of the Stick
(https://www.giantitp.com/comics/oots.html), comic images only.
"""

import re
from typing import Annotated

import typer
import typer.colors
from bs4 import BeautifulSoup
from rich import print as rprint

from oots_get import __version__
from oots_get.constants import (
    COMIC_TEMPLATE,
    COPYRIGHT_YEARS,
    HELP_STRING,
    OOTS_URL,
    OUTPUT_DIR,
)
from oots_get.helpers import (
    check_or_create_folder,
    clean_filename,
    get_last_comic,
    get_webpage,
    save_image,
)

app = typer.Typer(rich_markup_mode="rich", add_completion=False)


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

    rprint(
        f"oots-get (C) Grant Ramsay {COPYRIGHT_YEARS} (version {__version__})\n"
    )
    rprint(f"[cyan]Saving Comics to {OUTPUT_DIR}\n")

    check_or_create_folder(OUTPUT_DIR)

    # do specific depending on any command line arguements.
    last_id = get_last_comic() if only_new else 0

    # get the comic index webpage and parse the links
    bs = BeautifulSoup(get_webpage(OOTS_URL), "lxml")
    links = bs.find_all("p", attrs={"class": "ComicList"})
    for item in links:
        index, filename = item.text.split("-", 1)
        index = index.strip().zfill(4)

        # break here if we are only getting new comics
        if last_id >= int(index):
            break

        filename = clean_filename(index, filename)

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
