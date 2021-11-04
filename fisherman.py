#! /usr/bin/env python3

import json
import sys
from argparse import ArgumentParser
from base64 import b64decode
from datetime import datetime
from os import walk, remove, getcwd
from pathlib import Path
from re import findall
from time import sleep
from typing import Callable, List, AnyStr, Tuple
from zipfile import ZipFile, ZIP_DEFLATED

import colorama
import requests
import requests.exceptions
from selenium.common import exceptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.form_text import color_text
from src.logo import name
from src.manager import Manager, Xpaths

module_name = 'FisherMan: Extract information from facebook profiles.'
__version__ = "3.7.0"
__queue__ = []


class Fisher:
    def __init__(self):
        parser = ArgumentParser(description=f'{module_name} (Version {__version__})')
        exclusive_group = parser.add_mutually_exclusive_group()
        exclusive_group2 = parser.add_mutually_exclusive_group()

        opt_search = parser.add_argument_group("search options")
        opt_profile = parser.add_argument_group("profile options")
        opt_login = parser.add_argument_group("credentials")
        opt_out = parser.add_argument_group("output")
        exclusive_filter = opt_search.add_mutually_exclusive_group()
        exclusive_out = opt_out.add_mutually_exclusive_group()

        parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}',
                            help='Shows the current version of the program.')

        exclusive_group.add_argument('-u', '--username', nargs='+', help='Defines one or more users for the search.')

        exclusive_group.add_argument("-i", "--id", nargs="+", help="Set the profile identification number.")

        exclusive_group.add_argument('--use-txt', dest='txt', metavar='TXT_FILE', nargs=1,
                                     help='Replaces the USERNAME parameter with a user list in a txt.')

        exclusive_group.add_argument("-S", "--search", metavar="USER", help="It does a shallow search for the username."
                                                                            " Replace the spaces with '.'(period).")

        parser.add_argument("--update", action="store_true",
                            help="Check for changes with the remote repository to update.")

        exclusive_group2.add_argument('-v', '--verbose', action='store_true',
                                      help='It shows in detail the data search process.')

        exclusive_group2.add_argument("-q", "--quiet", action="store_true",
                                      help="Eliminates and simplifies some script outputs for "
                                           "a simpler and more discrete visualization.")

        opt_profile.add_argument('-sf', '--scrape-family', action='store_true', dest='scrpfm',
                                 help='If this parameter is passed, '
                                      'the information from family members will be scraped if available.')

        opt_profile.add_argument("--specify", nargs="+", type=int, choices=(0, 1, 2, 3, 4, 5),
                                 help="Use the index number to return a specific part of the page. "
                                      "about: 0, "
                                      "about_contact_and_basic_info: 1, "
                                      "about_family_and_relationships: 2, "
                                      "about_details: 3, "
                                      "about_work_and_education: 4, "
                                      "about_places: 5.")

        opt_profile.add_argument("-s", "--several", action="store_true",
                                 help="Returns extra data like profile picture, number of followers and friends.")

        opt_search.add_argument("--filters", action="store_true",
                                help="Shows the list of available filters.")

        exclusive_filter.add_argument("-work", help="Sets the work filter.")
        exclusive_filter.add_argument("-education", help="Sets the education filter.")
        exclusive_filter.add_argument("-city", help="Sets the city filter.")

        parser.add_argument('-b', '--browser', action='store_true', help='Opens the browser/bot.')

        opt_login.add_argument('--email', metavar='EMAIL', nargs=1,
                               help='If the profile is blocked, you can define your account, '
                                    'however you have the search user in your friends list.')

        opt_login.add_argument('--password', metavar='PASSWORD', dest='pwd', nargs=1,
                               help='Set the password for your facebook account, '
                                    'this parameter has to be used with --email.')

        exclusive_out.add_argument('-o', '--file-output', action='store_true', dest='out',
                                   help='Save the output data to a .txt file.')

        exclusive_out.add_argument("-c", "--compact", action="store_true",
                                   help="Save the output data to a .txt file and compress.")

        self.args = parser.parse_args()
        if not self.args.quiet:
            print(color_text('cyan', name))
        else:
            print("Starting FisherMan...")


def update():
    """
        checks changes from the main script to the remote server..
    """
    try:
        r = requests.get("https://raw.githubusercontent.com/Godofcoffe/FisherMan/main/fisherman.py")

        remote_version = str(findall('__version__ = "(.*)"', r.text)[0])
        local_version = __version__

        if remote_version != local_version:
            if not ARGS.quiet:
                print(color_text('yellow', "Update Available!\n" +
                                 f"You are running version {local_version}. Version {remote_version} "
                                 f"is available at https://github.com/Godofcoffe/FisherMan"))
            else:
                print(color_text("yellow", "Update Available!"))
    except Exception as error:
        print(color_text('red', f"A problem occured while checking for an update: {error}"))


def control(**kwargs):
    """
        Controls the flow of file updates.

        Use the key as an identifier for the function and this key will be displayed if the conditions are met,
        and use the function itself to rewrite the value.
    """
    start = []
    for process in kwargs.values():
        start.append(sub_update(process))

    for something_positive in start:
        if any(something_positive):
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
                print("nothing to update")


def sub_update(func):
    """
        Differentiates the contents of the local file with the remote file.

        :param func: function for the rewriting process.

        Just put the function you want to update a file from the remote server,
        for convenience put the name of the file in the function name, it can be anywhere,
        as long as the words are separated by underscores.
    """
    file_name = func.__name__.split("_")
    valid = []

    for _, _, files in walk(getcwd()):
        for file_ in files:
            for F in file_name:
                if F in file_:
                    try:
                        r2 = requests.get(f"https://raw.githubusercontent.com/Godofcoffe/FisherMan/main/{file_}")
                        if r2.text != open(f"{file_}").read():
                            print(color_text("yellow", f"Changes in the {file_} file have been found."))
                            __queue__.append(func)
                            valid.append(True)
                        else:
                            valid.append(False)
                    except Exception as error2:
                        print(color_text("red", f"A problem occurred when checking the {file_} file.\n{error2}"))
    return valid


def upgrade_filters():
    """
        Rewrite the filters.json file.
    """
    r3 = requests.get("https://raw.githubusercontent.com/Godofcoffe/FisherMan/main/filters.json")
    if r3.status_code == requests.codes.OK:
        with open("filters.json", "w") as new_filters:
            new_filters.write(r3.text)
    else:
        r3.raise_for_status()


def show_filters():
    """
        Shows the available filters.
    """
    with open("filters.json") as json_file:
        for tag in json.load(json_file).items():
            print(f"{tag[0]}:")
            for t in tag[1]:
                print("\t", t)


def upload_txt_file(name_file: AnyStr):
    """
        Load a file to replace the username parameter.

        :param name_file: txt file name.

        :return: A list with each line of the file.
    """
    if not name_file.endswith(".txt".lower()):
        name_file += ".txt"
    if Path(name_file).is_file():
        try:
            with open(name_file) as txt:
                users_txt = [line.replace("\n", "") for line in txt.readlines()]
        except Exception as error:
            print(color_text('red', f'An error has occurred: {error}'))
        else:
            return users_txt
    else:
        raise Exception(color_text("red", "INVALID FILE!"))


def compact(_list: List[AnyStr]):
    """
        Compress all .txt with the exception of requirements.txt.
    """
    out_file(_list)
    if ARGS.verbose:
        print(f'[{color_text("white", "*")}] preparing compaction...')
    with ZipFile(f"{str(datetime.now())[:16]}.zip", "w", ZIP_DEFLATED) as zip_output:
        for _, _, files in walk(getcwd()):
            for archive in files:
                extension = Path(archive).suffix
                _file_name = archive.replace(extension, "")
                if (extension.lower() == ".txt" and _file_name != "requeriments") or extension.lower() == ".png":
                    zip_output.write(archive)
                    remove(archive)
    print(f'[{color_text("green", "+")}] successful compression')


def check_connection():
    """
        Check the internet connection.
    """
    try:
        requests.get("https://google.com")
    except requests.exceptions.ConnectionError:
        raise Exception("There is no internet connection.")


def search(brw: Firefox, user: AnyStr):
    """
        It searches by the person's name.

        :param brw: Instance of WebDriver.
        :param user: name to search.
    """
    parameter = user.replace(".", "%20")

    with open("filters.json") as jsonfile:
        filters = json.load(jsonfile)
    if ARGS.work or ARGS.education or ARGS.city:
        suffix = "&filters="
        great_filter = ""
        if ARGS.work is not None:
            great_filter += filters["Work"][ARGS.work]
        elif ARGS.education is not None:
            great_filter += filters["Education"][ARGS.education]
        elif ARGS.city is not None:
            great_filter += filters["City"][ARGS.city]
        brw.get(f"{manager.get_search_prefix()}{parameter}{suffix + great_filter}")
    else:
        brw.get(f"{manager.get_search_prefix()}{parameter}")
    if ARGS.verbose:
        print(f'[{color_text("white", "+")}] entering the search page')
    sleep(2)
    profiles = scrolling_by_element(browser, (By.CSS_SELECTOR, "[role='article']"))
    if ARGS.verbose:
        print(f'[{color_text("green", "+")}] loaded profiles: {color_text("green", len(profiles))}')
    print(color_text("green", "Profiles found..."))
    print()
    for p in profiles:
        try:
            title = p.find_element_by_tag_name("h2")
        except (exceptions.StaleElementReferenceException, AttributeError, exceptions.NoSuchElementException):
            pass
        else:
            print(color_text("green", "Name:"), title.text)

        try:
            info = p.find_element_by_class_name("jktsbyx5").text
        except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
            pass
        else:
            print(color_text("green", "Info:"), str(info).replace("\n", ", "))

        try:
            link = str(title.find_element_by_css_selector("a[href]").get_attribute("href")).replace("\n", "")
        except (AttributeError, UnboundLocalError):
            pass
        else:
            print(color_text("green", "user|id:"), link)

        print()


def extra_data(brw: Firefox, user: AnyStr):
    """
        Save other data outside the about user page.

        :param brw: Instance of WebDriver.
        :param user: username to search.
    """
    if ARGS.id:
        brw.get(f"{manager.get_id_prefix() + user}")
    else:
        brw.get(f"{manager.get_url() + user}")

    friends = None

    wbw = WebDriverWait(brw, 10)
    xpaths = Xpaths()

    def collection_by_xpath(expected: Callable, xpath: AnyStr):
        try:
            wbw.until(expected((By.XPATH, xpath)))
        except exceptions.NoSuchElementException:
            print(f'[{color_text("red", "-")}] non-existent element')
        except exceptions.TimeoutException:
            if ARGS.verbose:
                print(f'[{color_text("yellow", "-")}] timed out to get the extra data')
            else:
                print(f'[{color_text("yellow", "-")}] time limit exceeded')
        else:
            return brw.find_element_by_xpath(xpath)

    img = collection_by_xpath(ec.element_to_be_clickable, xpaths.picture)
    img.screenshot(f"{user}_profile_picture.png")
    if not ARGS.quiet:
        print(f'[{color_text("green", "+")}] picture saved')

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
        element = element.find_elements_by_tag_name("span")[2].text
    except IndexError:
        print(f'[{color_text("red", "-")}] There is no number of friends to catch')
    except:
        friends = None
    else:
        friends = element

    if ARGS.txt:
        _file_name = rf"extraData-{user}-{str(datetime.now())[:16]}.txt"
        if ARGS.compact:
            _file_name = f"extraData-{user}.txt"
        with open(_file_name, "w+") as extra:
            extra.write(f"Bio: {bio}")
            extra.write(f"Followers: {followers}")
            extra.write(f"Friends: {friends}")
    else:
        # in the future to add more data variables, put in the dict
        manager.add_extras(user, {"Bio": bio, "Followers": followers, "Friends": friends})


def scrolling_by_element(brw: Firefox, locator: Tuple, n=30):
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
    while True:
        if len(elements) > n:
            break
        px += 250
        brw.execute_script(f"window.scroll(0, {px});")
        elements = brw.find_elements(*locator)
    return elements


def thin_out(user: AnyStr):
    """
        Username Refiner.

        :param user: user to be refined.

        This function returns a username that is acceptable for the script to run correctly.
    """

    if "id=" in user or user.isnumeric():
        if "facebook.com" in user:
            user = user[user.index("=") + 1:]
        return manager.get_id_prefix(), user
    else:
        if "facebook.com" in user:
            user = user[user.index("/", 9) + 1:]
        return manager.get_url(), user


def scrape(brw: Firefox, items: List[AnyStr]):
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
        prefix, usrs = thin_out(usrs)
        temp_data = []
        if not ARGS.quiet:
            print(f'[{color_text("white", "*")}] Coming in {prefix + usrs}')

        # here modifies the branch list to iterate only the parameter items --specify
        if ARGS.specify:
            temp_branch = []
            for index in ARGS.specify:
                temp_branch.append(branch[index])
                if ARGS.verbose:
                    print(f'[{color_text("green", "+")}] branch {index} added to url')
            branch = temp_branch

        # search for extra data
        if ARGS.several:
            if ARGS.verbose:
                print(f'[{color_text("blue", "+")}] getting extra data...')
            extra_data(brw, usrs)

        tot = len(branch)
        rest = 0
        for bn in branch if not usrs.isnumeric() else branch_id:
            brw.get(f'{prefix + usrs + bn}')
            try:
                output = wbw.until(ec.presence_of_element_located((By.CLASS_NAME, 'f7vcsfb0')))

            except exceptions.TimeoutException:
                print(f'[{color_text("yellow", "-")}] time limit exceeded')

            except Exception as error:
                print(f'[{color_text("red", "-")}] class f7vcsfb0 did not return')
                if ARGS.verbose:
                    print(color_text("yellow", f"error details:\n{error}"))
            else:
                if ARGS.verbose:
                    print(f'[{color_text("blue", "+")}] Collecting data from: div.f7vcsfb0')
                else:
                    if ARGS.quiet:
                        rest += 1
                        print("\033[K", f'[{color_text("blue", "+")}] collecting data ({rest}:{tot})', end="\r")
                    else:
                        print(f'[{color_text("blue", "+")}] collecting data ...')
                temp_data.append(output.text)

                # check to start scrape family members
                if "about_family_and_relationships" in bn:
                    members = output.find_elements(By.TAG_NAME, "a")
                    if members and ARGS.scrpfm:
                        members_list = []
                        for link in members:
                            members_list.append(link.get_attribute('href'))
                        manager.add_affluent(usrs, members_list)

        # this scope will only be executed if the list of "affluents" is not empty.
        if manager.get_affluent():
            div = "\n\n\n" + '=' * 60 + "\n\n\n"

            for memb in manager.get_affluent()[usrs]:
                print()
                if not ARGS.quiet:
                    print(f'[{color_text("white", "*")}] Coming in {memb}')
                temp_data.append(div)

                # search for extra data
                if ARGS.several:
                    if ARGS.verbose:
                        print(f'[{color_text("blue", "+")}] getting extra data...')
                    extra_data(brw, memb)

                rest = 0
                for bn in branch if not thin_out(memb)[1].isnumeric() else branch_id:
                    brw.get(f'{memb + bn}')
                    try:
                        output2 = wbw.until(ec.presence_of_element_located((By.CLASS_NAME,
                                                                            'f7vcsfb0')))

                    except exceptions.TimeoutException:
                        print(f'[{color_text("yellow", "-")}] time limit exceeded')

                    except Exception as error:
                        print(f'[{color_text("red", "-")}] class f7vcsfb0 did not return')
                        if ARGS.verbose:
                            print(color_text("yellow", f"error details:\n{error}"))
                    else:
                        if ARGS.verbose:
                            print(f'[{color_text("blue", "+")}] Collecting data from: div.f7vcsfb0')
                        else:
                            if ARGS.quiet:
                                rest += 1
                                print("\033[K", f'[{color_text("blue", "+")}] collecting data ({rest}:{tot})',
                                      end="\r")
                            else:
                                print(f'[{color_text("blue", "+")}] collecting data ...')
                        temp_data.append(output2.text)

        # complete addition of all data
        manager.add_data(usrs, temp_data)


def login(brw: Firefox):
    """
        Execute the login on the page.

        :param brw: Instance of WebDriver.
    """
    try:
        brw.get(manager.get_url())
    except exceptions.WebDriverException as error:
        if ARGS.verbose:
            print(f'[{color_text("red", "-")}] An error occurred while loading the home page:')
            print(error)
            print(f'[{color_text("yellow", "*")}] clearing cookies and starting over.')
        elif ARGS.quiet:
            print(f'[{color_text("yellow", "*")}] An error occurred, restarting.')

        brw.get(manager.get_url())
    finally:
        if brw.current_url != manager.get_url():
            print(color_text("red", "Unfortunately, I could not load the facebook homepage to login."))
            print(color_text("yellow", "Go to the repository and create a new issue reporting the problem."))
            sys.exit(1)

    wbw = WebDriverWait(brw, 10)

    email = wbw.until(ec.element_to_be_clickable((By.NAME, "email")))
    pwd = wbw.until(ec.element_to_be_clickable((By.NAME, "pass")))
    ok = wbw.until(ec.element_to_be_clickable((By.NAME, "login")))

    email.clear()
    pwd.clear()

    # custom accounts will only be applied if both fields are not empty
    if ARGS.email is None or ARGS.args.pwd is None:
        if ARGS.verbose:
            print(f'[{color_text("white", "*")}] adding fake email: {manager.get_email()}')
            email.send_keys(manager.get_email())
            print(f'[{color_text("white", "*")}] adding password: ...')
            pwd.send_keys(b64decode(manager.get_pass()).decode("utf-8"))
        else:
            print(f'[{color_text("white", "*")}] logging into the account: {manager.get_email()}')
            email.send_keys(manager.get_email())
            pwd.send_keys(b64decode(manager.get_pass()).decode("utf-8"))
    else:
        if ARGS.verbose:
            print(f'adding email: {ARGS.email}')
            email.send_keys(ARGS.args.email)
            print('adding password: ...')
            pwd.send_keys(ARGS.pwd)
        else:
            print(f'logging into the account: {ARGS.email}')
            email.send_keys(ARGS.email)
            pwd.send_keys(ARGS.pwd)
    ok.click()
    if ARGS.verbose:
        print(f'[{color_text("green", "+")}] successfully logged in')


def init():
    """
        Start the webdriver.
    """

    # browser settings
    _options = Options()

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

    if not ARGS.browser:
        if ARGS.verbose:
            print(f'[{color_text("blue", "*")}] Starting in hidden mode')
        _options.headless = True
    _options.add_argument("--start-maximized")

    if ARGS.verbose:
        print(f'[{color_text("white", "*")}] Opening browser ...')
    try:
        engine = Firefox(options=_options)
    except Exception as error:
        print(color_text("red",
                         f'The executable "geckodriver" was not found or the browser "Firefox" is not installed.'))
        print(color_text("yellow", f"error details:\n{error}"))
    else:
        return engine


def out_file(_input: List[AnyStr]):
    """
        Create the .txt output of the -o parameter.

        :param _input: The list that will be iterated over each line of the file, in this case it is the list of users.
    """
    for usr in _input:
        usr = thin_out(usr)[1]
        file_name = rf"{usr}-{str(datetime.now())[:16]}.txt"
        if ARGS.compact:
            file_name = usr + ".txt"
        with open(file_name, 'w+') as file:
            for data_list in manager.get_data()[usr]:
                file.writelines(data_list)

    print(f'[{color_text("green", "+")}] .txt file(s) created')


if __name__ == '__main__':
    colorama.init()
    check_connection()
    fs = Fisher()
    manager = Manager()
    ARGS = fs.args
    if ARGS.update:
        update()
        control(filters=upgrade_filters)  # add more parameters as you add files to update.
        sys.exit(0)
    if ARGS.filters:
        show_filters()
        sys.exit(0)
    if not ARGS.id and not ARGS.username and not ARGS.txt and not ARGS.search:
        print(f"No input argument was used.")
        print(f"Use an optional argument to run the script.")
        print(f"Use --help.")
        sys.exit(1)
    browser = init()
    try:
        login(browser)
        if ARGS.search:
            search(browser, ARGS.search)
        elif ARGS.txt:
            scrape(browser, upload_txt_file(ARGS.txt[0]))
        elif ARGS.username:
            scrape(browser, ARGS.username)
        elif ARGS.id:
            scrape(browser, ARGS.id)
    except Exception as error:
        raise error
    finally:
        browser.quit()
    if ARGS.out:
        if ARGS.username:
            out_file(ARGS.username)
        elif ARGS.txt:
            out_file(upload_txt_file(ARGS.txt[0]))
        elif ARGS.id:
            out_file(ARGS.id)

    elif ARGS.compact:
        if ARGS.username:
            compact(ARGS.username)
        elif ARGS.txt:
            compact(upload_txt_file(ARGS.txt[0]))
        elif ARGS.id:
            compact(ARGS.id)

    else:
        if ARGS.id or ARGS.username or ARGS.txt:
            print(color_text('green', 'Information found:'))
        count_profiles = len(manager.get_all_keys()[2])
        for profile in manager.get_all_keys()[2]:
            for data in manager.get_data()[profile]:
                print('-' * 60)
                print(data)
            if count_profiles > 1:
                print("\n\n")
                print("-" * 30, "{:^}".format("/" * 20), "-" * 28)
                print("\n\n")

            if ARGS.several:
                print("=" * 60)
                print("EXTRAS:")
                for data_extra in manager.get_extras()[profile].items():
                    print(f"{data_extra[0]:10}: {data_extra[1]}")
