from logidoor.libs.cli.progressbar import printg
from logidoor.libs.cli.printf import *


def send_form_auth(browser, url, username, password, result):
    # Limit length of string using format
    # https://stackoverflow.com/a/24076314
    if not browser.login_form.entry_text:
        printg(f"Password: \033[95m{password:50.50}\033[0m")
    else:
        printg(f"Username: \033[96m{username:29.29}\033[0m Password: \033[95m{password:29.29}\033[0m")

    browser.open(url)
    if not browser.find_login_form():
        # print_error("Can't find login form for current thread")
        return

    resp = browser.login(username, password)
    browser.refresh()

    if not browser.find_login_form():
        for this_url in browser.get_page_redirection(resp.text):
            if this_url:
                if not this_url.startswith("http"):
                    # URL can be Absolute URLs vs. Relative URLs
                    # When URL is Relative, we can use urljoin as stackoverflow bellow
                    # from urllib.parse import urljoin
                    # check_url = urljoin(url, this_url)
                    # https://stackoverflow.com/a/44002598
                    # Or use open_relative which is mentioned in the doc, follow_link part
                    browser.open_relative(this_url)
                else:
                    browser.open(this_url)
                if browser.find_login_form():
                    return False
        try:
            title = browser.page.title.text
        except AttributeError:
            title = "No title"
        print_info(f"Title: {title}")
        print_info(f"HTTP Status code: {resp.status_code}")

        # A verbose like message to print new contents
        # When tool gets false positives, attacker knows using the output msg
        import html2text
        convert = html2text.HTML2Text()
        contents_change = browser.get_page_change(resp.text).strip()
        new_contents = convert.handle(contents_change).strip()
        if new_contents.count("\n") < 2:
            print_info(new_contents)

        browser.session.cookies.clear()
        browser.session.close()

        if browser.login_form.entry_text:
            print_found(username, password)
            result.put([url, username, password])
            return True
        else:
            print_found(None, password)
            result.put([url, None, password])
            return True

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
