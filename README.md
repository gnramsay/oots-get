# oots-get

[![PyPI version fury.io](https://badge.fury.io/py/oots-get.svg)](https://pypi.python.org/pypi/oots-get/)
[![PyPI license](https://img.shields.io/pypi/l/oots-get.svg)](https://pypi.python.org/pypi/oots-get/)
[![PyPI status](https://img.shields.io/pypi/status/oots-get.svg)](https://pypi.python.org/pypi/oots-get/)

This is a simple Python script to maintain a local archive of the web comic
['The Order of the Stick'][oots], though can probably be modified reasonably
easily for others if required.

This is a __work in progress__ although base functionality is working perfectly.

Primarily an exercise in using ['Beautiful Soup'][bs] with a live target. Also I
love this comic and when I originally wrote it I often spent  a lot of time
without any internet.

This is a rewrite from scratch of my original Ruby script of the same name.

## Usage

### Install

Using pipx to install globally (recommended) :

```bash
pipx install oots-get
```

Or use pip:

```bash
pip install oots-get
```

### Quick start

Run the script :

```bash
oots-get
```

This will parse the OOTS website, then download any missing comics. These comics
will be stored in the `comics/oots` subdirectory of the users home directory by
default though this will be changable shortly via settings file.

This package has been tested to work under both Linux and Windows 10.

## Configuration File

To be added.

## Command line switches

- `--only-new` ( short form: `-n`) : only check for new up to the last comic
  already downloaded, this speeds up operation.

## To-Do

see the [TODO.md](TODO.md) file.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

I'll add a proper CONTRIBUTING.md file soon.

## Copyright

(C) Grant Ramsay (<grant@gnramsay.com>) 2021-2024.

[oots]: http://www.giantitp.com/comics/oots.html
[bs]: https://www.crummy.com/software/BeautifulSoup/
