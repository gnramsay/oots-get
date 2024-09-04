"""Helper functions for the OOTS get CLI."""

import os
import re
import shutil
from pathlib import Path

import requests
import typer
from rich import print as rprint

from oots_get.constants import OUTPUT_DIR, STATUS_OK


def get_webpage(page_url: str) -> str:
    """Get the OOTS index webpage and return the content."""
    result = requests.get(page_url, timeout=10)
    if result.status_code == STATUS_OK:
        return result.text

    rprint(
        "Unable to read the OOTS data,please check your connection.",
    )
    rprint("URL : %s", page_url)
    raise typer.Exit(code=1)


def check_or_create_folder(folder_path: Path) -> None:
    """Check if the provided folder exists, and create if not.

    :param folder_path: Path to folder to create.
    :type folder_path: String
    """
    folder_path.mkdir(parents=True, exist_ok=True)


def get_last_comic() -> int:
    """Return the index number of the last (highest) comic downloaded."""
    return int(sorted(os.listdir(OUTPUT_DIR), reverse=True)[0].split("-")[0])


def clean_filename(index: str, filename: str) -> str:
    """Clean up the filename and add the index at the start."""
    filename = filename.strip().replace(" ", "-").replace("/", "-")
    filename = re.sub(r"[?:.#,!'\"]", "", filename)
    return f"{index}-{filename}"


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
