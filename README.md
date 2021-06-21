# Goal data collection
The objective of this task is to collect test data through web scraping to simulate the
scenario of users typing in their free text goals.

## Installation
Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install requirements.
```bash
pip3 install -r requirements.txt
```

## Usage
This is an example of how to run crawler ith a trigger phrase is "My goal is to", and the number of results to collect are 5:

```bash
python3 crawler.py -tp "My goal is to" -n 5
```

Or you can get help with the command:
```bash
python3 crawler.py --help
```