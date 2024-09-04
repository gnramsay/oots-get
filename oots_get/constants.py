"""Define constants used throughout the package."""

from pathlib import Path

OOTS_URL: str = "https://www.giantitp.com/comics/oots.html"
COMIC_TEMPLATE: str = "https://www.giantitp.com/comics/oots{index}.html"
OUTPUT_DIR: Path = Path(Path.home() / "comics" / "oots")

STATUS_OK = 200
HELP_STRING = "Download the 'Order of the Stick' comics locally."
COPYRIGHT_YEARS = "2013-2024"
