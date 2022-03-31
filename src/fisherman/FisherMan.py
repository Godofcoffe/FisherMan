import json
import sys
from base64 import b64decode
from datetime import datetime
from os import remove, getcwd, scandir
from pathlib import Path
from re import findall
from time import sleep
from typing import Callable, List, AnyStr, Tuple
from zipfile import ZipFile, ZIP_DEFLATED

import colorama
import requests
import requests.exceptions
from selenium.common import exceptions
from selenium.webdriver import Firefox, Edge, DesiredCapabilities
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from .scripts.form_text import color_text
from .scripts.logo import name
from .manager import Manager, Xpaths

module_name = 'FisherMan: Extract information from facebook profiles.'
__version__ = "3.9"
__queue__ = [] # list of functions that have updated files


class GenericException(Exception):
    msg = f"Something wrong happened here.\nReport in: https://github.com/Godofcoffe/FisherMan/issues"


    def __init__(self, **kwargs):
        super().__init__(self.msg, **kwargs)


    def __call__(self, func: Callable) -> Callable:
        def exception(*args, **kwargs):
            try:
                data = func(*args, **kwargs)
            except Exception as error:
                raise GenericException
        return exception


class Fisher(Manager):
    def __init__(self, parser):
        self.args = parser
        if not self.args.quiet:
            if not self.args.blackout:
                print(color_text('cyan', name))
            else:
                print(name)
        else:
            print("Starting FisherMan...")
        if not self.args.blackout:
            colorama.init()
        self.check_connection()


    def update(self) -> None:
        """
            checks changes from the main script to the remote server..
        """
        try:
            r = requests.get("https://raw.githubusercontent.com/Godofcoffe/FisherMan/main/src/fisherman/FisherMan.py")

            remote_version = str(findall('__version__ = "(.*)"', r.text)[0])
            local_version = __version__

            if remote_version != local_version:
                if not self.args.quiet:
                    if not self.args.blackout:
                        print(color_text('yellow', "Update Available!\n" +
                                        f"You are running version {local_version}. Version {remote_version} "
                                        f"is available at https://github.com/Godofcoffe/FisherMan"))
                    else:
                        print("Update Available!\n" +
                             f"You are running version {local_version}. Version {remote_version} "
                             f"is available at https://github.com/Godofcoffe/FisherMan")
                else:
                    if not self.args.blackout:
                        print(color_text("yellow", "Update Available!"))
                    else:
                        print("Update Available!")
        except Exception as error:
            if not self.args.blackout:
                print(color_text('red', f"A problem occured while checking for an update: {error}"))
            else:
                print(f"A problem occured while checking for an update: {error}")

        self.__control(filters=self._upgrade_filters) # add more parameters as you add files to update.


    @GenericException()
    def __control(self, **kwargs) -> None:
        """
            Controls the flow of file updates.

            Use the key as an identifier for the function and this key will be displayed if the conditions are met,
            and use the function itself to rewrite the value.
        """
        for process in kwargs.values():
            start = self.__sub_update(process)

        # checks if a file is "True", and searches for the related function to update.
        if any(start):
            print("Updates are available:")
            if __queue__:
                for func in __queue__:
                    for key in kwargs.keys():
                        if key in func.__name__:
                            print(key)
                print()
                choose = input("Continue?[Y/N]: ").strip().lower()[0]
                if choose == "y":
                    for obsolete in __queue__:
                        obsolete()
        else:
            print("Nothing to update")


    def __sub_update(self, func) -> List[bool]:
        """
            Differentiates the contents of the local file with the remote file.

            :param func: function for the rewriting process.

            Just put the function you want to update a file from the remote server,
            for convenience put the name of the file in the function name, it can be anywhere,
            as long as the words are separated by underscores.
        """
        file_name = func.__name__.split("_")
        valided = []
        wasteds = []
        relevant_directories = ['.', './src/fisherman/']

        for path in relevant_directories:
            for arch in scandir(path):
                for split in file_name:
                    if split in arch.name and split:
                        wasteds.append(arch)
                        continue

        if wasteds:
            for wasted in wasteds:
                try:
                    raw = open(f"{wasted.path}").read()
                except FileNotFoundError:
                    if not self.args.blackout:
                        print(color_text("yellow", f"File {wasted.name} not found"))
                    else:
                        print(f"File {wasted.name} not found")
                    if self.args.verbose:
                        print('Trying again...')
                    try:
                        raw = open(f"{wasted.path}").read()
                    except:
                        if not self.args.blackout:
                            print(color_text('red',
                                             'Maybe the file is not located in the expected path'))
                        else:
                            print('Maybe the file is not located in the expected path')
                else:
                    try:
                        r2 = requests.get('https://raw.githubusercontent.com/'
                                          f'Godofcoffe/FisherMan/main/src/fisherman/{wasted.name}')
                    except:
                        if not self.args.blackout:
                            print(color_text('red', 'File not found in the repository'))
                        else:
                            print('File not found in the repository')
                        r2 = requests.get('https://raw.githubusercontent.com/'
                                          f'Godofcoffe/FisherMan/main/{wasted.name}')
                    else:
                        if r2.text != raw:
                            if not self.args.blackout:
                                print(color_text("yellow", f"Changes in the {wasted.name} file have been found"))
                            else:
                                print(f"Changes in the {wasted.name} file have been found")
                                # Add the function that will change the file to a global update list
                                __queue__.append(func)
                                valided.append(True)
                        else:
                            valided.append(False)
        return valided # returns the signal of the files ready to change.


    def _upgrade_filters(self) -> None:
        """
            Rewrite the filters.json file.
        """
        r3 = requests.get("https://raw.githubusercontent.com/"
                          "Godofcoffe/FisherMan/main/src/fisherman/filters.json")
        if r3.status_code == requests.codes.OK:
            with open("./src/fisherman/filters.json", "w") as new_filters:
                new_filters.write(r3.text)
        else:
            r3.raise_for_status()


    @GenericException()
    def show_filters(self) -> None:
        """
            Shows the available filters.
        """
        with open("./src/fisherman/filters.json") as json_file:
            for tag in json.load(json_file).items():
                print(f"{tag[0]}:")
                for t in tag[1]:
                    print("\t", t)


    def __upload_txt_file(self, name_file) -> List[str]:
        """
            Load a file to replace the username parameter.
        """
        if not name_file.endswith(".txt"):
            name_file += ".txt"
        if Path(name_file).is_file():
            try:
                with open(name_file) as txt:
                    users_txt = [line.replace("\n", "") for line in txt.readlines()]
            except Exception as error:
                if not self.args.blackout:
                    print(color_text('red', f'An error has occurred: {error}'))
                else:
                    print(f'An error has occurred: {error}')
            else:
                return users_txt
        else:
            raise FileExistsError(
                    color_text("red", "INVALID FILE!") if not self.args.blackout else print("INVALID FILE!")
                )


    def entry(self, name_file: str) -> List[str]:
        """
            Load a file to replace the username parameter.

            :param name_file: txt file name.

            :return: A list with each line of the file.
        """
        self.__upload_txt_file(name_file)


    def __compact(self, _list) -> None:
        """
            Create a zip of all the program's outputs.
        """
        __out_file(_list)
        if self.args.verbose:
            if not self.args.blackout:
                print(f'[{color_text("white", "*")}] preparing compaction...')
            else:
                print('[*] preparing compaction...')
        with ZipFile(f"{datetime.now():%d-%m-%Y-%H-%M}.zip", "w", ZIP_DEFLATED) as zip_output:
            for _, _, files in walk(getcwd()):
                for archive in files:
                    extension = Path(archive).suffix
                    _file_name = archive.replace(extension, "")
                    if (extension.lower() == ".txt" and _file_name != "requeriments") or extension.lower() == ".png":
                        zip_output.write(archive)
                        remove(archive)
        if not self.args.blackout:
            print(f'[{color_text("green", "+")}] successful compression')
        else:
            print('[+] successful compression')


    @GenericException()
    def save_and_compact(self, _list: List[str]) -> None:
        """
            Create a zip of all the program's outputs.

            :param _input: The list that will be iterated over each line of the file, in this case it is the list of users.
        """
        self.__compact(_list)



    def check_connection(self) -> None:
        """
            Check the internet connection.
        """
        try:
            requests.get("https://google.com")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("There is no internet connection")


    @GenericException()
    def _search(self, brw, user: AnyStr) -> None:
        """
            It searches by the person's name.

            :param brw: Instance of WebDriver.
            :param user: name to search.
        """
        parameter = user.replace(".", "%20")

        with open("./src/fisherman/filters.json") as jsonfile:
            filters = json.load(jsonfile)

        if self.args.work or self.args.education or self.args.city:
            suffix = "&filters="
            great_filter = ""
            if self.args.work is not None:
                great_filter += filters["Work"][self.args.work]
            elif self.args.education is not None:
                great_filter += filters["Education"][self.args.education]
            elif self.args.city is not None:
                great_filter += filters["City"][self.args.city]
            brw.get(f"{self.get_search_prefix()}{parameter}{suffix + great_filter}")
        else:
            brw.get(f"{self.get_search_prefix()}{parameter}")

        if self.args.verbose:
            if not self.args.blackout:
                print(f'[{color_text("white", "+")}] entering the search page')
            else:
                print('[+] entering the search page')
        sleep(2)
        profiles = self.__scrolling_by_element(brw, (By.CSS_SELECTOR, "[role='article']"))
        if self.args.verbose:
            if not self.args.blackout:
                print(f'[{color_text("green", "+")}] loaded profiles: {color_text("green", len(profiles))}')
            else:
                print(f'[+] loaded profiles: {len(profiles)}')


        if not self.args.blackout:
            print(color_text("green", "Profiles found..."))
        else:
            print('Profiles found...')
        print()
        for profile in profiles:
            try:
                title = profile.find_element(By.TAG_NAME, "h2")
            except (exceptions.StaleElementReferenceException, AttributeError, exceptions.NoSuchElementException):
                pass
            else:
                if not self.args.blackout:
                    print(color_text("green", "Name:"), title.text)
                else:
                    print("Name: ", title.text)

            try:
                info = profile.find_element(By.CLASS_NAME, "jktsbyx5").text
            except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                pass
            else:
                if not self.args.blackout:
                    print(color_text("green", "Info:"), str(info).replace("\n", ", "))
                else:
                    print('Info: ', str(info).replace("\n", ", "))

            try:
                link = str(title.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href")).replace("\n", "")
            except (AttributeError, UnboundLocalError):
                pass
            else:
                if not self.args.blackout:
                    print(color_text("green", "user|id:"), link)
                else:
                    print('user|id: ', link)
            print()


    # As much as extra_data and scrape() do not return, 
    # the generated data is saved in the global Manager class as a dictionary.


    # Use Manager.get_data(), to return all dictionaries, 
    # or get.all_...() for a tuple with specific information.


    def _extra_data(self, brw, user: AnyStr) -> None:
        """
            Save other data outside the about user page.

            :param brw: Instance of WebDriver.
            :param user: username to search.
        """
        if self.args.id:
            brw.get(f"{self.get_id_prefix() + user}")
        else:
            brw.get(f"{self.get_url() + user}")

        friends = None

        wbw = WebDriverWait(brw, 10)
        xpaths = Xpaths()

        def collection_by_xpath(expected: Callable, xpath: AnyStr):
            try:
                wbw.until(expected((By.XPATH, xpath)))
            except exceptions.NoSuchElementException:
                if not self.args.blackout:
                    print(f'[{color_text("red", "-")}] non-existent element')
                else:
                    print('[-] non-existent element')
            except exceptions.TimeoutException:
                if self.args.verbose:
                    if not self.args.blackout:
                        print(f'[{color_text("yellow", "-")}] timed out to get the extra data')
                    else:
                        print('[-] timed out to get the extra data')
                else:
                    if not self.args.blackout:
                        print(f'[{color_text("yellow", "-")}] time limit exceeded')
                    else:
                        print('[-] time limit exceeded')
            else:
                return brw.find_element_by_xpath(xpath)

        img = collection_by_xpath(ec.element_to_be_clickable, xpaths.picture)
        img.screenshot(f"{user}_profile_picture.png")
        if not self.args.quiet:
            if not self.args.blackout:
                print(f'[{color_text("green", "+")}] picture saved')
            else:
                print('[+] picture saved')

        try:
            element = collection_by_xpath(ec.visibility_of_element_located, xpaths.bio).text
        except AttributeError:
            bio = None
        else:
            bio = element

        if collection_by_xpath(ec.visibility_of_element_located, xpaths.followers) is not None:
            followers = str(collection_by_xpath(ec.visibility_of_element_located, xpaths.followers).text).split()[0]
        else:
            followers = None

        try:
            element = collection_by_xpath(ec.visibility_of_element_located, xpaths.friends)
            element = element.find_elements(By.TAG_NAME, "span")[2].text
        except IndexError:
            if not self.args.blackout:
                print(f'[{color_text("red", "-")}] There is no number of friends to catch')
            else:
                print('[-] There is no number of friends to catch')
        except:
            friends = None
        else:
            friends = element

        if self.args.txt:
            _file_name = f"extraData-{user}-{str(datetime.now()):%d-%m-%yy-%h-%M}.txt"
            if self.args.compact:
                _file_name = f"extraData-{user}.txt"
            with open(_file_name, "w+") as extra:
                extra.write(f"Bio: {bio}")
                extra.write(f"Followers: {followers}")
                extra.write(f"Friends: {friends}")
        else:
            # in the future to add more data variables, put in the dict
            self.add_extras(user, {"Bio": bio, "Followers": followers, "Friends": friends})


    def __scrolling_by_element(self, brw, locator: Tuple, n=30) -> List:
        """
            Scroll page by the number of elements.

            :param brw: Instance of WebDriver.
            :param locator: The element tuple as a "locator". Example: (By.NAME, "foo").
            :param n: The number of elements you want it to return.

            The page will scroll until the condition n is met, the default value of n is 30.

        """
        wbw = WebDriverWait(brw, 10)
        px = 0
        elements = wbw.until(ec.presence_of_all_elements_located(locator))
        while len(elements) < n:
            px += 250
            brw.execute_script(f"window.scroll(0, {px});")
            elements = brw.find_elements(*locator)
        return elements


    def __thin_out(self, user: AnyStr) -> AnyStr:
        """
            Username Refiner.

            :param user: user to be refined.

            This function returns a username that is acceptable for the script to run correctly.
        """

        if "id=" in user or user.isnumeric():
            if "facebook.com" in user:
                user = user[user.index("=") + 1:]
            return self.get_id_prefix(), user
        else:
            if "facebook.com" in user:
                user = user[user.index("/", 9) + 1:]
            return self.get_url(), user


    @GenericException()
    def _scrape(self, brw, items: List[AnyStr]) -> None:
        """
            Extract certain information from the html of an item in the list provided.

            :param brw: Instance of WebDriver.
            :param items: List of users to apply to scrape.

            All data is stored in a list for each iterable items.
        """

        branch = ['/about', '/about_contact_and_basic_info', '/about_family_and_relationships', '/about_details',
                '/about_work_and_education', '/about_places']
        branch_id = [bn.replace("/", "&sk=") for bn in branch]
        wbw = WebDriverWait(brw, 10)

        for usrs in items:
            prefix, usrs = self.__thin_out(usrs)
            temp_data = []
            if not self.args.quiet:
                if not self.args.blackout:
                    print(f'[{color_text("white", "*")}] Coming in {prefix + usrs}')
                else:
                    print(f'[*] coming in {prefix + usrs}')

            # here modifies the branch list to iterate only the parameter items --specify
            if self.args.specify:
                temp_branch = []
                for index in self.args.specify:
                    temp_branch.append(branch[index])
                    if self.args.verbose:
                        if not self.args.blackout:
                            print(f'[{color_text("green", "+")}] branch {index} added to url')
                        else:
                            print(f'[+] branch {index} added to url')
                branch = temp_branch

            # search for extra data
            if self.args.several:
                if self.args.verbose:
                    if not self.args.blackout:
                        print(f'[{color_text("blue", "+")}] getting extra data...')
                    else:
                        print('[+] getting extra data...')
                _extra_data(brw, usrs)

            tot = len(branch)
            rest = 0
            for bn in branch if not usrs.isnumeric() else branch_id:
                brw.get(f'{prefix + usrs + bn}')
                try:
                    output = wbw.until(ec.presence_of_element_located((By.CLASS_NAME, 'f7vcsfb0')))

                except exceptions.TimeoutException:
                    if not self.args.blackout:
                        print(f'[{color_text("yellow", "-")}] time limit exceeded')
                    else:
                        print('[-] time limit exceeded')

                except Exception as error:
                    if not self.args.blackout:
                        print(f'[{color_text("red", "-")}] class f7vcsfb0 did not return')
                    else:
                        print('[-] class f7vcsfb0 did not return')
                    if self.args.verbose:
                        if not self.args.blackout:
                            print(color_text("yellow", f"error details:\n{error}"))
                        else:
                            print(f"error details:\n{error}")
                else:
                    if self.args.verbose:
                        if not self.args.blackout:
                            print(f'[{color_text("blue", "+")}] Collecting data from: div.f7vcsfb0')
                        else:
                            print('[+] collecting data from: div.f7vcsfb0')
                    else:
                        if self.args.quiet:
                            rest += 1
                            if not self.args.blackout:
                                print("\033[K", f'[{color_text("blue", "+")}] collecting data ({rest}:{tot})', end="\r")
                            else:
                                print("\033[K", f'[+] collecting data ({rest}:{tot})', end="\r")
                        else:
                            if not self.args.blackout:
                                print(f'[{color_text("blue", "+")}] collecting data...')
                            else:
                                print('[+] collecting data...')
                    temp_data.append(output.text)

                    # check to start scrape family members
                    if "about_family_and_relationships" in bn:
                        members = output.find_elements(By.TAG_NAME, "a")
                        if members and self.args.scrpfm:
                            members_list = []
                            for link in members:
                                members_list.append(link.get_attribute('href'))
                            self.add_affluent(usrs, members_list)

            # this scope will only be executed if the list of "affluents" is not empty.
            if self.get_affluent():
                div = "\n\n\n" + '=' * 60 + "\n\n\n"

                for memb in self.get_affluent()[usrs]:
                    print()
                    if not self.args.quiet:
                        if not self.args.blackout:
                            print(f'[{color_text("white", "*")}] Coming in {memb}')
                        else:
                            print(f'[*] comming in {memb}')
                    temp_data.append(div)

                    # search for extra data
                    if self.args.several:
                        if self.args.verbose:
                            if not self.args.blackout:
                                print(f'[{color_text("blue", "+")}] getting extra data...')
                            else:
                                print('[+] getting extra data...')
                        _extra_data(brw, memb)

                    rest = 0
                    for bn in branch if not self.__thin_out(memb)[1].isnumeric() else branch_id:
                        brw.get(f'{memb + bn}')
                        try:
                            output2 = wbw.until(ec.presence_of_element_located((By.CLASS_NAME,
                                                                                'f7vcsfb0')))

                        except exceptions.TimeoutException:
                            if not self.args.blackout:
                                print(f'[{color_text("yellow", "-")}] time limit exceeded')
                            else:
                                print('[-] time limit exceeded')

                        except Exception as error:
                            if not self.args.blackout:
                                print(f'[{color_text("red", "-")}] class f7vcsfb0 did not return')
                            else:
                                print('[-] class f7vcsfb0 did not return')
                            if self.args.verbose:
                                if not self.args.blackout:
                                    print(color_text("yellow", f"error details:\n{error}"))
                                else:
                                    print(f"error details:\n{error}")
                        else:
                            if self.args.verbose:
                                if not self.args.blackout:
                                    print(f'[{color_text("blue", "+")}] Collecting data from: div.f7vcsfb0')
                                else:
                                    print('[+] collecting data from: div.f7vcsfb0')
                            else:
                                if self.args.quiet:
                                    rest += 1
                                    if not self.args.blackout:
                                        print("\033[K",
                                             f'[{color_text("blue", "+")}] collecting data ({rest}:{tot})',
                                             end="\r")
                                    else:
                                        print("\033[K", f'[+] collecting data ({rest}:{tot})', end="\r")
                                else:
                                    if not self.args.blackout:
                                        print(f'[{color_text("blue", "+")}] collecting data...')
                                    else:
                                        print('[+] collecting data...')
                            temp_data.append(output2.text)

            # complete addition of all data
            self.add_data(usrs, temp_data)


    def __login(self, brw) -> None:
        """
            Execute the login on the page.
        """
        url_base = self.get_url()

        try:
            brw.get(url_base)
        except exceptions.WebDriverException as error:
            if self.args.verbose:
                if not self.args.blackout:
                    print(f'[{color_text("red", "-")}] An error occurred while loading the home page:')
                    print(error)
                    print(f'[{color_text("yellow", "*")}] clearing cookies and starting over.')
                else:
                    print('[-] An error occurred while loading the home page:')
                    print(error)
                    print('[*] clearing cookies and starting over')
            elif self.args.quiet:
                if not self.args.blackout:
                    print(f'[{color_text("yellow", "*")}] An error occurred, restarting.')
                else:
                    print('[*] An error occurred, restarting')

            brw.delete_all_cookies()
            self.__login(brw)
        finally:
            if brw is None or (brw.current_url != url_base):
                if not self.args.blackout:
                    print(color_text("red", "Unfortunately, I could not load the facebook homepage to login."))
                    print(color_text("yellow", "Go to the repository and create a new issue reporting the problem."))
                else:
                    print("Unfortunately, I could not load the facebook homepage to login.")
                    print("Go to the repository and create a new issue reporting the problem.")

        wbw = WebDriverWait(brw, 10)

        email = wbw.until(ec.element_to_be_clickable((By.NAME, "email")))
        pwd = wbw.until(ec.element_to_be_clickable((By.NAME, "pass")))
        ok = wbw.until(ec.element_to_be_clickable((By.NAME, "login")))

        email.clear()
        pwd.clear()

        # custom accounts will only be applied if both fields are not empty
        if self.args.email is None or self.args.pwd is None:
            ghost_email = self.get_email()
            ghost_pass = self.get_pass()

            if self.args.verbose:
                if not self.args.blackout:
                    print(f'[{color_text("white", "*")}] adding ghost email: {ghost_email}')
                else:
                    print(f'[*] adding ghost email: {ghost_email}')
                email.send_keys(ghost_email)

                if not self.args.blackout:
                    print(f'[{color_text("white", "*")}] adding password:...')
                else:
                    print('[*] adding password:...')
                pwd.send_keys(b64decode(ghost_pass).decode("utf-8"))
            else:
                if not self.args.blackout:
                    print(f'[{color_text("white", "*")}] logging into the account: {ghost_email}')
                else:
                    print(f'[*] logging into the account: {ghost_email}')
                email.send_keys(ghost_email)
                pwd.send_keys(b64decode(ghost_pass).decode("utf-8"))
        else:
            if self.args.verbose:
                print(f'adding email: {self.args.email}')
                email.send_keys(self.args.email)
                print('adding password:...')
                pwd.send_keys(self.args.pwd)
            else:
                print(f'logging into the account: {self.args.email}')
                email.send_keys(self.args.email)
                pwd.send_keys(self.args.pwd)
        ok.click()
        if self.args.verbose:
            if not self.args.blackout:
                print(f'[{color_text("green", "+")}] successfully logged in')
            else:
                print('[+] successfully logged in')


    def login_in(self, browser) -> None:
        """
            Login on the page.

            :param browser: Instance of WebDriver.
        """

        self.__login(browser)


    def __who_is(self):
        """
        It takes the OS and returns the corresponding webdriver.
        """
        if "win" in sys.platform:
            return (Edge, EdgeOptions(), "./bin/msedgedriver.exe")
        else:
            return (Firefox, FirefoxOptions(), "./bin/geckodriver")


    def boot(self) -> Firefox:
        """
            Start the webdriver.
        """


        driver, _options, _path = self.__who_is()

        capability = ["--incognito",
                      "--disable-extensions",
                      "--disable-plugins-discovery",
                      "--start-maximized"
                    ]

        hidden = False

        if not self.args.browser:
            if self.args.verbose:
                if not self.args.blackout:
                    print(f'[{color_text("blue", "*")}] Starting in hidden mode')
                else:
                    print('[*] starting in hidden mode')
            hidden = True

        if self.args.verbose:
            if not self.args:
                print(f'[{color_text("white", "*")}] Opening browser...')
            else:
                print('[*] opening browser...')
        
        if isinstance(driver, Edge):
            if hidden:
                capability.append("--headless")
            _options.set_capability("args", capability)
        else:
            if self.args.proxy:
                prox_http = self.args.proxy
                if self.args.verbose:
                    if not self.args.blackout:
                        print("[{1}] activated: proxy({0})".format(
                                                                    color_text("yellow", self.args.proxy),
                                                                    color_text("yellow", "*")
                                                                )
                             )
                    else:
                        print(f"[*] activated: proxy({self.args.proxy})")

                # prox_https = "<>"
                DesiredCapabilities.FIREFOX["proxy"] = {
                    "httpProxy": prox_http,
                    "proxyType": "MANUAL",
                }

            if self.args.dom:
                if self.args.verbose:
                    if not self.args.blackout:
                        print("[{1}] activated {0}".format(
                                                        color_text("yellow", "only_DOM"),
                                                        color_text("yellow", "*")
                                                        )
                             )
                    else:
                        print("[*] activated: only_DOM")
                _options.page_load_strategy = "eager"


            _options.add_argument("--start-maximized")

            # eliminate pop-ups
            _options.set_preference("dom.popup_maximum", 0)
            _options.set_preference("privacy.popups.showBrowserMessage", False)

            # incognito
            _options.set_preference("browser.privatebrowsing.autostart", True)
            _options.add_argument("--incognito")

            # arguments
            # _options.add_argument('--disable-blink-features=AutomationControlled')
            _options.add_argument("--disable-extensions")
            # _options.add_argument('--profile-directory=Default')
            _options.add_argument("--disable-plugins-discovery")

            if hidden:
                _options.headless = True

        try:
            engine = driver(executable_path=_path, options=_options)

        except Exception as error:
            message = 'The executable "geckodriver/msedgedriver.exe" ' \
                      'was not found or the browser "Firefox" is not installed.'
            if not self.args.blackout:
                print(color_text("red", message))
                print(color_text("yellow", f"error details:\n{error}"))
            else:
                print(message)
                print(f"error details:\n{error}")

            print("Trying the default system path....")

            try:
                engine = driver(options=_options)
            except Exception as error:
                if not self.args.blackout:
                    print(color_text("red", message))
                    print(color_text("yellow", f"error details:\n{error}"))
                else:
                    print(message)
                    print(f"error details:\n{error}")
        else:
            return engine


    def __out_file(self, _input) -> None:
        """
            Create the .txt output of the -o parameter.
        """
        for usr in _input:
            usr = self.__thin_out(usr)[1]
            file_name = f"{usr}:{datetime.now():%d-%m-%Y-%H-%M}.txt"
            if self.args.compact:
                file_name = usr + ".txt"
            with open(file_name, 'w+') as file:
                for data_list in self.get_data()[usr]:
                    file.writelines(data_list)

        if not self.args.blackout:
            print(f'[{color_text("green", "+")}] .txt file(s) created')
        else:
            print('[+] .txt file(s) created')


    @GenericException()
    def save(self, _input: List[str]) -> None:
        """
            Create the .txt output of the -o parameter.

            :param _input: The list that will be iterated over each line of the file, in this case it is the list of users.
        """
        self.__out_file(_input)
