# FisherMan

[![GitHub license](https://img.shields.io/github/license/Godofcoffe/FisherMan)](https://github.com/Godofcoffe/FisherMan/blob/main/LICENSE)
![badge](https://img.shields.io/badge/version-3.8-blue)
![badge](https://img.shields.io/badge/python-%3E%3D3.8-orange)

### Search for public profile information on Facebook

![demo-gif](demo-fisherman.gif)

## Installation

```console
# clone the repo
$ git clone https://github.com/Godofcoffe/FisherMan.git

# change the working directory to FisherMan and change the branch
$ cd FisherMan
$ git switch compatible-with-windows

# change the branch
$ git switch compatible-with-windows

# install the requeriments
$ python3 -m pip install -r requeriments.txt

# dependency:
 Download the chromedriver driver from this link:
 http://chromedriver.storage.googleapis.com/index.html
 And paste the .exe into the **bin** folder inside the program.
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
<<<<<<< HEAD
$ python3 fisherman.py --help
usage: fisherman.py [-h] [--version] [-u [USERNAME ...] | -i [ID ...] |
                    --use-txt TXT_FILE | -S USER] [--update] [--blackout]
                    [-v | -q] [-sf] [--specify [{0,1,2,3,4,5} ...]] [-s]
=======
$ py fisherman.py --help
usage: fisherman.py [-h] [--version] [-u USERNAME [USERNAME ...] | -i ID
                    [ID ...] | --use-txt TXT_FILE | -S USER] [-v | -q] [-sf]
                    [--specify {0,1,2,3,4,5} [{0,1,2,3,4,5} ...]] [-s]
>>>>>>> fa660f0 (Update README.md)
                    [--filters]
                    [-work WORK | -education EDUCATION | -city CITY] [-b]
                    [--email EMAIL] [--password PASSWORD] [-o | -c]

FisherMan: Extract information from facebook profiles. (Version 3.8)

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

<<<<<<< HEAD
* User name: `python3 fisherman.py -u name.profile name.profile2`
* ID: `python3 fisherman.py -i 000000000000`
=======
* User name: `py fisherman.py -u name name.profile name.profile2`
* ID: `py fisherman.py -i 000000000000`
>>>>>>> fa660f0 (Update README.md)

The username must be found on the facebook profile link, such as:

```
https://facebook.com/name.profile/
```

It is also possible to load multiple usernames from a .txt file, this can be useful for a brute force output type:

```
py fisherman.py --use-txt filename.txt
```

Some profiles are limited to displaying your information for any account, so you can use your account to extract. Note:
this should be used as the last hypothesis, and the target profile must be on your friends list:

```
py fisherman.py --email youremail@email.com --password yourpass
```

### Some situations:

* For complete massive scrape:
  ```
  py fisherman.py --use-txt file -c -sf
  ```
  With a file with dozens of names on each line, you can make a complete "scan" taking your information and even your
  family members and will be compressed into a .zip at the output.

* For specific parts of the account:
<<<<<<< HEAD
    * Basic data: `python3 fisherman.py -u name --specify 0`
    * Family and relationship: `python3 -u name --specify 2`
    * It is still possible to mix: `python3 fisherman.py -u name --specify 0 2`
    * Association of the pages:
      ```
      about: 0
      about_contact_and_basic_info: 1
      about_family_and_relationships: 2
      about_details: 3
      about_work_and_education: 4
      about_places: 5
      ```
=======
    * Basic data: `py fisherman.py -u name --specify 0`
    * Family and relationship: `py -u name --specify 2`
    * It is still possible to mix: `py fisherman.py -u name --specify 0 2`

>>>>>>> fa660f0 (Update README.md)

* To get additional things like profile picture, how many followers and how many friends:
  ```
  py fisherman.py -u name [-s | --several]
  ```
  
* For a short search by people's name:
  ```
<<<<<<< HEAD
  python3 fisherman.py [-S | --search] The.Fisherman
=======
  py fisherman.py [-S | --search] foo
>>>>>>> fa660f0 (Update README.md)
  ```
  Replace the spaces in the name with "."(periods).
  The script returns around 30 profiles.

* To filter the search:
  ```
  py fisherman.py -S name -work fisherman
  ```
  If the filter has spaces, enclose it in quotes.
  
* For a minimalist execution:
  ```
  py fisherman.py [-q | --quiet]
  ```
  Considerably reduces the script's output texts and, by convention, improves performance.

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
