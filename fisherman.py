<<<<<<< HEAD
#! /usr/bin/env python3

=======
import json
import sys
>>>>>>> 30892b1f7286563801c60529ac3e4df99be833fa
from argparse import ArgumentParser

<<<<<<< HEAD
from src.fisherman.FisherMan import Fisher, __version__, module_name, color_text
=======
import colorama
import requests
import requests.exceptions
from selenium.common import exceptions
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.chrome.options import Options as Chrome_options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as Firefox_options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.form_text import color_text
from src.logo import name
from src.manager import Manager, Xpaths

module_name = 'FisherMan: Extract information from facebook profiles.'
__version__ = "3.7.1"
__queue__ = []
>>>>>>> 30892b1f7286563801c60529ac3e4df99be833fa



footer = "If you want to see examples of usage and a specific argument.\n" \
         "See: https://github.com/Godofcoffe/FisherMan#usage"

parser = ArgumentParser(description=f'{module_name} (Version {__version__})', epilog=footer)
exclusive_group = parser.add_mutually_exclusive_group()
exclusive_group2 = parser.add_mutually_exclusive_group()

opt_search = parser.add_argument_group("search options")
opt_profile = parser.add_argument_group("profile options")
opt_login = parser.add_argument_group("credentials")
opt_out = parser.add_argument_group("output")

exclusive_filter = opt_search.add_mutually_exclusive_group()
exclusive_out = opt_out.add_mutually_exclusive_group()

parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}',
                    help='shows the current version of the program')

exclusive_group.add_argument('-u', '--username', nargs='*', help='defines one or more users for the search')

exclusive_group.add_argument("-i", "--id", nargs="*", help="set the profile identification number")

exclusive_group.add_argument('--use-txt', dest='txt', metavar='TXT_FILE',
                            help='replaces the USERNAME parameter with a user list in a txt')

exclusive_group.add_argument("-S", "--search", metavar="USER", help="it does a shallow search for the username."
                                                                    " Replace the spaces with '.'(period)")

parser.add_argument("--update", action="store_true",
                    help="check for changes with the remote repository to update")

parser.add_argument("--blackout", action="store_true", help="disable colors")

exclusive_group2.add_argument('-v', '--verbose', action='store_true',
                              help='it shows in detail the data search process')

exclusive_group2.add_argument("-q", "--quiet", action="store_true",
                              help="eliminates and simplifies some script outputs for "
                                   "a simpler and discrete visualization")

opt_profile.add_argument('-sf', '--scrape-family', action='store_true', dest='scrpfm',
                         help='if this parameter is passed, '
                              'the information from family members will be scraped if available')

opt_profile.add_argument("--specify", nargs="*", type=int, choices=(0, 1, 2, 3, 4, 5),
                         help="use the index number to return a specific part of the page")

opt_profile.add_argument("-s", "--several", action="store_true",
                         help="returns extra data like profile picture, number of followers and friends")

opt_search.add_argument("--filters", action="store_true",
                        help="shows the list of available filters")

exclusive_filter.add_argument("-work", help="sets the work filter")
exclusive_filter.add_argument("-education", help="sets the education filter")
exclusive_filter.add_argument("-city", help="sets the city filter")

parser.add_argument('-b', '--browser', action='store_true', help='opens the browser/bot')

opt_login.add_argument('--email', metavar='EMAIL',
                        help='if the profile is blocked, you can define your account, '
                            'however you have the search user in your friends list')

opt_login.add_argument('--password', metavar='PASSWORD', dest='pwd',
                            help='set the password for your facebook account, '
                                 'this parameter HAS to be used with --email')

exclusive_out.add_argument('-o', '--file-output', action='store_true', dest='out',
                                help='save the output data to a .txt file')

exclusive_out.add_argument("-c", "--compact", action="store_true",
                                help="save the output data to a .txt file and compress")


cli = parser.parse_args()

little_fish = Fisher(parser=cli)

if cli.filters:
    little_fish.show_filters()
elif cli.update:
    little_fish.update()
elif any((cli.id, cli.username, cli.search, cli.txt)):
    browser = little_fish._boot()
    try:
        little_fish.login_in(browser)
    except Exception as error:
        print(error)
    else:
        if cli.search:
            little_fish._search(browser, cli.search)
        else:
            if cli.txt:
                little_fish._scrape(browser, little_fish.entry(cli.txt))
            elif cli.username:
                little_fish._scrape(browser, cli.username)
            elif cli.id:
                little_fish._scrape(browser, cli.id)

            if little_fish.get_data() and (not cli.out and not cli.compact):
                if not cli.blackout:
                    print(color_text('green', 'Information found:'))
                else:
                    print('Information found:')
                count_profiles = len(little_fish.get_all_keys()[2])
                for profile in little_fish.get_all_keys()[2]:
                    for data in little_fish.get_data()[profile]:
                        print('-' * 60)
                        print(data)
                    if count_profiles > 1:
                        print("\n\n")
                        print("-" * 30, "{:^}".format("/" * 20), "-" * 28)
                        print("\n\n")

                    if cli.several:
                        print("=" * 60)
                        print("EXTRAS:")
                        for data_extra in little_fish.get_extras()[profile].items():
                            print(f"{data_extra[0]:10}: {data_extra[1]}")
            elif little_fish.get_data() and (cli.out or cli.compact):
                if cli.out:
                    if cli.username:
                        little_fish.save(cli.username)
                    elif cli.txt:
                        little_fish.save(little_fish.entry(cli.txt))
                    elif cli.id:
                        little_fish.save(cli.id)

                elif cli.compact:
                    if cli.username:
                        little_fish.save_and_compact(cli.username)
                    elif cli.txt:
                        little_fish.save_and_compact(little_fish.entry(cli.txt))
                    elif cli.id:
                        little_fish.save_and_compact(cli.id)
            else:
                print("Forgive me, I couldn't find anything.")
    finally:
<<<<<<< HEAD
        if browser is not None:
            browser.quit()
else:
    print(f"No input argument was used.")
    print(f"Use an optional argument to run the script.")
    print(f"Use --help.")
=======
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
    # browser options
    _options = Chrome_options()
    _options.add_argument("--incognito")
    _options.add_argument("--disable-extensions")
    _options.add_argument("--disable-plugins-discovery")

    if not ARGS.browser:
        if ARGS.verbose:
            print(f'[{color_text("blue", "*")}] Starting in hidden mode')
        _options.add_argument("--headless")
    else:
        _options.add_argument("--start-maximized")

    if ARGS.verbose:
        print(f'[{color_text("white", "*")}] Opening browser ...')
    try:
        engine = Chrome(options=_options, executable_path="./bin/chromedriver.exe")
    except:
        print(color_text("red",
                         f'The executable "chromedriver" was not found or the browser "Chrome" is not installed.'))
        print("Trying with the Firefox browser.")
        # browser settings
        del _options
        _options = Firefox_options()

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
            _options.add_argument("--headless")
        else:
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
>>>>>>> 30892b1f7286563801c60529ac3e4df99be833fa
