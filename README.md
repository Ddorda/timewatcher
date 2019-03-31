# Timewatcher

Timewatcher is a [Timewatch](https://www.timewatch.co.il/) auto filler

## Requirements

* Chrome(ium?)
* chromium-chromedriver
* python-selenium

To install requirements on Ubuntu:

```sh
$ sudo apt-get install chromium-chromedriver python-selenium
$ git clone https://github.com/Ddorda/timewatcher.git
```

(if someone wanna add how to install on windows would be awesome)

## Execution

```sh
$ cd timewatcher
$ ./timewatcher.py
```

On first execution you'll be asked for your login credentials, which will be saved on same directory in `config.json` for later executions.