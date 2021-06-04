import argparse
from logidoor.resources import wordlists
from logidoor.libs.utils import *
import sys


def get_wordlists():
    # Listing all modules https://stackoverflow.com/q/8529192
    # Check if object is function https://stackoverflow.com/a/4202642
    wordlist_user = []
    wordlist_passwd = []
    for func_name, obj in wordlists.__dict__.items():
        if hasattr(obj, '__call__'):
            if func_name.endswith("_pass"):
                wordlist_passwd.append(func_name.split("_")[0])
            elif func_name.endswith("_user"):
                wordlist_user.append(func_name.split("_")[0])
            else:
                pass
    all_lists = [x for x in wordlist_user if x in wordlist_passwd]
    return wordlist_user, wordlist_passwd, all_lists


pre_user_list, pre_passwd_list, pre_usr_passwd_lists = get_wordlists()


def parse_options():
    parser = argparse.ArgumentParser(description="Automation HTTP web-from Brute-Forcer")
    group_core = parser.add_argument_group("Core options")
    group_core.add_argument(
        "-u",
        "--url",
        help="Target URL"
    )
    group_core.add_argument(
        "-uL",
        "--url-list",
        help="Path to file contains URL"
    )
    group_core.add_argument(
        "-p",
        "--proxy",
        help="User proxy (not supported in this version)"  # todo work on here
    )
    group_core.add_argument(
        "-t",
        "--threads",
        type=int,
        help="Number of threads",
        default=16
    )

    group_wordlist = parser.add_argument_group("Wordlist")
    group_wordlist.add_argument(
        "-un",
        "--username",
        help="Username. Support multiple user by :"
    )
    group_wordlist.add_argument(
        "-uF",
        "--user-list",
        help="Path to username wordlist"
    )
    group_wordlist.add_argument(
        "-pn",
        "--password",
        help="Password"
    )
    group_wordlist.add_argument(
        "-pF",
        "--pass-list",
        help="Path to password wordlist"
    )
    group_wordlist.add_argument(
        "-uW",
        "--pre-user-list",
        help=f"Select prebuild username wordlist. Choices: {pre_user_list}",
        metavar="Wordlist",
        choices=pre_user_list
    )
    group_wordlist.add_argument(
        "-pW",
        "--pre-pass-list",
        help=f"Select prebuild password wordlist. Choices: {pre_passwd_list}",
        metavar="Wordlist",
        choices=pre_passwd_list
    )
    group_wordlist.add_argument(
        "-wl",
        "--pre-wordlist",
        help=f"Select prebuild wordlist for username and password. Choices: {pre_usr_passwd_lists}",
        metavar="Wordlist",
        choices=pre_usr_passwd_lists
    )
    group_wordlist.add_argument(
        "-pM",
        "--pass-mask",
        help="Generate password from mask",
        metavar="awWds"
    )
    # TODO gen sqli
    if len(sys.argv) == 1:
        parser.print_help()
        exit()
    return parser


class ProgOptions:
    def __init__(self):
        args = parse_options()
        self.user_options = args.parse_args()
        self.url = self.__validate_url_option()
        self.user_list = self.__is_user_list()
        self.threads = self.__validate_threads()

    def get_pass_list(self):
        if self.user_options.password:
            for password in set(self.user_options.password):
                yield password
        elif self.user_options.pass_list:
            # TODO runtime file handle here
            return tuple(set(filter(None, file_read(self.user_options.pass_list).split("\n"))))
        elif self.user_options.pre_pass_list:
            if self.user_options.pre_pass_list in pre_passwd_list:
                module = getattr(wordlists, f"{self.user_options.pre_pass_list}_pass")
                for password in set(module().split("\n")):
                    yield password
            else:
                raise ValueError("Invalid name of prebuild password wordlist")
        elif self.user_options.pre_wordlist:
            if self.user_options.pre_wordlist in pre_usr_passwd_lists:
                module = getattr(wordlists, f"{self.user_options.pre_wordlist}_pass")
                for password in set(module().split("\n")):
                    yield password
            else:
                raise ValueError("Invalid name of prebuild password wordlist")
        elif self.user_options.pass_mask:
            from itertools import product
            for password in product(*self.__parse_pass_mask(), repeat=1):
                yield password
        else:
            module = getattr(wordlists, "default_pass")
            for password in set(module().split("\n")):
                yield password

    def get_user_list(self):
        if self.user_options.username:
            for username in set(self.user_options.username.split(":")):
                yield username
        elif self.user_options.user_list:
            # TODO handle runtime file read here
            return set(filter(None, file_read(self.user_options.user_list).split("\n")))
        elif self.user_options.pre_user_list:
            if self.user_options.pre_user_list in pre_user_list:
                module = getattr(wordlists, f"{self.user_options.pre_user_list}_user")
                for username in set(module().split("\n")):
                    yield username
            else:
                raise ValueError("Invalid name of prebuild username wordlist")
        elif self.user_options.pre_wordlist:
            if self.user_options.pre_wordlist in pre_usr_passwd_lists:
                module = getattr(wordlists, f"{self.user_options.pre_wordlist}_user")
                for username in set(module().split("\n")):
                    yield username
            else:
                raise ValueError("Invalid name of prebuild username wordlist")

    def __validate_url_option(self):
        def validate_url_format(url):
            if not url:
                return url
            if "://" not in url:
                return "http://" + url
            else:
                return url

        if self.user_options.url_list:
            return tuple(set(filter(
                None,
                (validate_url_format(x) for x in file_read(self.user_options.url_list).split("\n"))
            )))
        elif self.user_options.url:
            return tuple({validate_url_format(self.user_options.url)})
        else:
            raise ValueError("URL address is required")

    def __is_user_list(self):
        if self.user_options.username or self.user_options.user_list or self.user_options.pre_userlist or \
                self.user_options.pre_wordlist:
            return True
        return False

    def __parse_pass_mask(self):
        import string
        charsets = []

        for mask in self.user_options.pass_mask:
            if mask == "a":
                charsets.append(tuple(string.ascii_letters))
            elif mask == "w":
                charsets.append(tuple(string.ascii_lowercase))
            elif mask == "W":
                charsets.append(tuple(string.ascii_uppercase))
            elif mask == "d":
                charsets.append(tuple(string.digits))
            elif mask == "s":
                charsets.append(tuple(string.punctuation))
        return charsets

    def __validate_threads(self):
        try:
            return int(self.user_options.threads)
        except Exception:
            raise Exception("Invalid thread options")
