from logidoor.libs.cli.progressbar import printg
from logidoor.libs.cli.printf import *


def send_form_auth(browser, url, username, password, result):
    # Limit length of string using format
    # https://stackoverflow.com/a/24076314
    if not browser.login_form.entry_text:
        printg(f"Password: \033[95m{password:50.50}\033[0m")
    else:
        printg(f"Username: \033[96m{username:29.29}\033[0m Password: \033[95m{password:29.29}\033[0m")
    browser.login(username, password)
    # TODO analysis more from here
    # We are going to use score base system
    # Title page change
    # No login form
    # HTML contents change
    if not browser.find_login_form():
        if not browser.check_login_redirection():
            if browser.login_form.entry_text:
                print_found(username, password)
                result.put([url, username, password])
                return True
            else:
                print_found(None, password)
                result.put([url, None, password])
                return True
    else:
        return False


def send_basic_auth(browser, url, username, password, result):
    printg(f"Username: \033[96m{username:29.29}\033[0m Password: \033[95m{password:29.29}\033[0m")
    resp = browser.open(url, auth=(username, password))
    if resp.status_code == 401:
        pass
    elif resp.status_code >= 400:
        print_error(f"{resp.status_code} for \"\033[96m{username}\033[0m\":\"\033[95m{password}\033[0m\"")
    else:
        print_found(username, password)
        result.put([url, username, password])
