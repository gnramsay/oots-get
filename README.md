# oots-get

[![PyPI version fury.io](https://badge.fury.io/py/oots-get.svg)](https://pypi.python.org/pypi/oots-get/)
[![PyPI license](https://img.shields.io/pypi/l/oots-get.svg)](https://pypi.python.org/pypi/oots-get/)
[![PyPI status](https://img.shields.io/pypi/status/oots-get.svg)](https://pypi.python.org/pypi/oots-get/)

This is a simple Python script to maintain a local archive of the web comic
['The Order of the Stick'][oots], though can probably be modified reasonably
easily for others if required.

This is a __work in progress__ although base functionality is working perfectly.

Primarily an exercise in using ['Beautiful Soup'][bs] with a live target. Also I
love this comic and often spend time without internet.

This is a rewrite from scratch of my original Ruby script of the same name.

## Usage

### Install

```python
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

Not in any specific order :

- Improve error-checking and recovery
- Add command line options to modify configuration, and a config file. Any
  options on command line to have precedence over settings specified in the
  configuration file.
- Add command line options for quiet as well as the existing verbose, with same
  options in the config file.
- Option to save log file for each run.
- Add testing!
- ~~Add colours to the output, just because.~~
- ~~Add option to start checking at the last downloaded comic instead of
  start.~~

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## Building

### Create an 'editable' install

From the root of the project, run the following which will install an editable
version of the package. This updates as you change the source, so no need to
keep reinstalling the package to test :

```bash
pip install -e .
```

(Do not forget the tailing period!)

### Build Package

Install dependencies :

```bash
pip install -r requirements.txt
```

Run Tests. There are only dummy tests at the moment, this will change shortly :

```bash
pytest
```

To create the source and wheel packages :

```bash
python -m build
```

Build documentation (from the docs subdiretory) :

```bash
make html
```

## Copyright

(C) Grant Ramsay (grant@gnramsay.com) 2021.

[oots]: http://www.giantitp.com/comics/oots.html
[bs]: https://www.crummy.com/software/BeautifulSoup/
