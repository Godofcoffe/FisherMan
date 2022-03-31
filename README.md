<div align=center>

  <img src="media/logo.png" style="width:200px;"></img>

  [![GitHub license](https://img.shields.io/github/license/Godofcoffe/FisherMan)](https://github.com/Godofcoffe/FisherMan/blob/main/LICENSE)
  ![badge](https://img.shields.io/badge/version-3.9-blue)
  ![badge](https://img.shields.io/badge/python-%3E%3D3.8-orange)

</div>

<div align=center>
  <h3>Search for public profile information on Facebook</h3>
  <img src="media/demo-fisherman.gif"></img>
</div>

## Installation
**Warning: The Windows compatibility script has been merged with the pricipal.**
```console
# clone the repo
$ git clone https://github.com/Godofcoffe/FisherMan

# change the working directory to FisherMan
$ cd FisherMan

# install the requeriments
$ [python3 or py] -m pip install -r requeriments.txt

# dependency:
you need to Download geckodriver(for Linux) or msedgedriver.exe(for Windows) on your machine,
download the binary from the official repos:

* https://github.com/mozilla/geckodriver/releases/latest
* https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

extract and copy the binary, put it in the *bin* folder inside the program.
```

## Docker

### Build

```console
docker build . -t fisherman
```

### run
```console
docker run --rm -it fisherman --help
```

## Usage

```console
$ python3 fisherman.py --help
usage: fisherman.py [-h] [--version] [-u [USERNAME ...] | -i [ID ...] |
                    --use-txt TXT_FILE | -S USER] [--update] [--blackout]
                    [-v | -q] [-sf] [--specify [{0,1,2,3,4,5} ...]]
                    [-s | --only-dom] [--filters]
                    [-work WORK | -education EDUCATION | -city CITY] [-b]
                    [--email EMAIL] [--password PASSWORD]
                    [--proxy [HOST:PORT]] [-o | -c]

FisherMan: Extract information from facebook profiles. (Version 3.9)

options:
  -h, --help            show this help message and exit
  --version             shows the current version of the program
  -u [USERNAME ...], --username [USERNAME ...]
                        defines one or more users for the search
  -i [ID ...], --id [ID ...]
                        set the profile identification number
  --use-txt TXT_FILE    replaces the USERNAME parameter with a user list in a
                        txt
  -S USER, --search USER
                        it does a shallow search for the username. Replace the
                        spaces with '.'(period)
  --update              check for changes with the remote repository to update
  --blackout            disable colors
  -v, --verbose         it shows in detail the data search process
  -q, --quiet           eliminates and simplifies some script outputs for a
                        simpler and discrete visualization
  -b, --browser         opens the browser/bot
  --proxy [HOST:PORT]   define a proxy server to use

search options:
  --filters             shows the list of available filters
  -work WORK            sets the work filter
  -education EDUCATION  sets the education filter
  -city CITY            sets the city filter

profile options:
  -sf, --scrape-family  if this parameter is passed, the information from
                        family members will be scraped if available
  --specify [{0,1,2,3,4,5} ...]
                        use the index number to return a specific part of the
                        page
  -s, --several         returns extra data like profile picture, number of
                        followers and friends
  --only-dom            only the DOM/text of the page is used

credentials:
  --email EMAIL         if the profile is blocked, you can define your
                        account, however you have the search user in your
                        friends list
  --password PASSWORD   set the password for your facebook account, this
                        parameter HAS to be used with --email

output:
  -o, --file-output     save the output data to a .txt file
  -c, --compact         save the output data to a .txt file and compress
```

To search for a user:

* User name: `python3 fisherman.py -u name.profile name.profile2`
* ID: `python3 fisherman.py -i 000000000000`

The username must be found on the facebook profile link, such as:

```
https://facebook.com/name.profile/
```

It is also possible to load multiple usernames from a .txt file, this can be useful for a brute force output type:

```
python3 fisherman.py --use-txt filename.txt
```

Some profiles are limited to displaying your information for any account, so you can use your account to extract. Note:
this should be used as the last hypothesis, and the target profile must be on your friends list:

```
python3 fisherman.py --email youremail@email.com --password yourpass
```

### Some situations:

* For complete massive scrape:
  ```
  python3 fisherman.py --use-txt file -c -sf
  ```
  With a file with dozens of names on each line, you can make a complete "scan" taking your information and even your
  family members and will be compressed into a .zip at the output.

* For specific parts of the account:
    * Basic data: `python3 fisherman.py -u name --specify 0`
    * Family and relationship: `python3 -u name --specify 2`
    * It is still possible to mix: `python3 fisherman.py -u name --specify 0 2`
    * Association of the pages:
      ```
      about: 0
      about contact and basic info: 1
      about family and relationships: 2
      about details: 3
      about work and education: 4
      about places: 5
      ```

* To get additional things like profile picture, how many followers and how many friends:
  ```
  python3 fisherman.py -u name [-s | --several]
  ```
  
* For a short search by people's name:
  ```
  python3 fisherman.py [-S | --search] The.Fisherman
  ```
  Replace the spaces in the name with "."(periods).
  The script returns around 30 profiles.

* To filter the search:
  ```
  python3 fisherman.py -S name -work fisherman
  ```
  If the filter has spaces, enclose it in quotes.
  
* For a minimalist execution:
  ```
  python3 fisherman.py [-q | --quiet]
  ```
  Considerably reduces the script's output texts and, by convention, improves performance.

* Using proxies:
  ```
  python3 fisherman.py -u name --proxy
  ```
  A default server will be used, but you can still set a server that you think is best `--proxy <HOST:PORT>`, but I recommend that it should not be too far away from the US region so that the account is not at risk of being blocked.

  And there is still the option of a small optimization of the page, making the browser load only the DOM and disabling media such as images. Using:
    ```
    python3 fisherman.py -u name --proxy --only-dom
    ```

## Contributing
I would love to have your help in developing this project.

Some things you can help me with:
  * Add more search filters.

Please look at the Wiki entry on [Adding filters to the search argument](https://github.com/Godofcoffe/FisherMan/wiki/Adding-filters-to-the-search-argument) to understand the issues.

## *This tool only extracts information that is public, not use for private or illegal purposes.*
_This is a legacy project, I have no guarantee that its functionality will be working in the future, because it does not apply some of Selenium's best practices._

## LICENSE

BSD 3-Clause © FisherMan Project

Original Creator - [Godofcoffe](https://github.com/Godofcoffe)
