#! /usr/bin/env python3

from argparse import ArgumentParser

from src.fisherman.FisherMan import Fisher, __version__, module_name



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
                little_fish._scrape(browser, little_fish.entry(cli.txt[0]))
            elif cli.username:
                little_fish._scrape(browser, cli.username)
            elif cli.id:
                little_fish._scrape(browser, cli.id)
            print(color_text('green', 'Information found:'))
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
    finally:
        browser.quit()

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
    print(f"No input argument was used.")
    print(f"Use an optional argument to run the script.")
    print(f"Use --help.")
