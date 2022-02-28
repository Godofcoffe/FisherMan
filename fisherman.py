#! /usr/bin/env python3

from argparse import ArgumentParser

from src.fisherman.FisherMan import Fisher, __version__, module_name



def parser():
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

    exclusive_group.add_argument('-u', '--username', nargs='*', help='Defines one or more users for the search.')

    exclusive_group.add_argument("-i", "--id", nargs="*", help="Set the profile identification number.")

    exclusive_group.add_argument('--use-txt', dest='txt', metavar='TXT_FILE',
                                help='Replaces the USERNAME parameter with a user list in a txt.')

    exclusive_group.add_argument("-S", "--search", metavar="USER", help="It does a shallow search for the username."
                                                                        " Replace the spaces with '.'(period).")

    parser.add_argument("--update", action="store_true",
                        help="Check for changes with the remote repository to update.")

    parser.add_argument("--blackout", action="store_true", help="Disable colors.")

    exclusive_group2.add_argument('-v', '--verbose', action='store_true',
                                    help='It shows in detail the data search process.')

    exclusive_group2.add_argument("-q", "--quiet", action="store_true",
                                  help="Eliminates and simplifies some script outputs for "
                                        "a simpler and more discrete visualization.")

    opt_profile.add_argument('-sf', '--scrape-family', action='store_true', dest='scrpfm',
                             help='If this parameter is passed, '
                                    'the information from family members will be scraped if available.')

    opt_profile.add_argument("--specify", nargs="*", type=int, choices=(0, 1, 2, 3, 4, 5),
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

    opt_login.add_argument('--email', metavar='EMAIL',
                            help='If the profile is blocked, you can define your account, '
                                 'however you have the search user in your friends list.')

    opt_login.add_argument('--password', metavar='PASSWORD', dest='pwd',
                            help='Set the password for your facebook account, '
                                 'this parameter has to be used with --email.')

    exclusive_out.add_argument('-o', '--file-output', action='store_true', dest='out',
                                help='Save the output data to a .txt file.')

    exclusive_out.add_argument("-c", "--compact", action="store_true",
                                help="Save the output data to a .txt file and compress.")
    return parser.parse_args()


little_fish = Fisher(parser=parser())
browser = little_fish._boot()
