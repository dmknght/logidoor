from logidoor.libs.cli.progressbar import printg
from logidoor.libs.cli.printf import *


def login_analysis(browser, url, resp, first_login_form):
    if not resp.text:
        return False
    new_contents = browser.get_page_contents(resp.text)
    changed_contents = [x for x in new_contents if x not in browser.first_content]
    if len(changed_contents) < 2:
        print_info(changed_contents, "DIFF")
        return False
    else:
        # Changed content includes link. We try to compare how many URLs in current contents
        # If link changed < 2: return false
        # print(browser.first_content)
        # print(new_contents)
        # print(changed_contents)
        # print([x for x in new_contents if x not in changed_contents])
        # print(f"Link counts: {browser.count_page_contents_urls(resp.text)}")
        # Analysis URL from source code
        for this_url in browser.get_page_redirection(resp.text, url):
            # When login, website can show web panel or error page "failed to login. click here to go back"
            # Metasploitable 2, tomcat server port 8180 is an example
            # We can try get all URLs then click on each URL to check if it goes to login page
            # False positive: If web panel has "logout" URL, the whole result will be wrong
            # The only solution is analysis response and get the totally different responses
            if this_url and "logout" not in this_url:
                resp = browser.open(this_url, verify=False)
                if resp.status_code >= 400:
                    return False
                check_login_form = browser.find_login_form()
                if check_login_form:
                    if check_login_form.__dict__ != first_login_form.__dict__:
                        print_warn(f"Login form is different from the first one")
                        try:
                            title = browser.page.title.text
                        except AttributeError:
                            title = "No title"
                        print_info(f"Title: {title}", info=resp.status_code)
                    return False
                else:
                    try:
                        title = browser.page.title.text
                    except AttributeError:
                        title = "No title"
                    print_info(f"Title: {title}", info=resp.status_code)
                    return True


def send_form_auth(browser, url, username, password, proxy, result):
    # Limit length of string using format
    # https://stackoverflow.com/a/24076314
    browser.auto_set_proxy(proxy)
    browser.auto_set_ua()
    if not browser.login_form.entry_text:
        printg(f"Password: \033[95m{password:50.50}\033[0m")
    else:
        printg(f"Username: \033[96m{username:29.29}\033[0m Password: \033[95m{password:29.29}\033[0m")

    browser.open(url, verify=False)
    first_login_form = browser.find_login_form()
    if not first_login_form:
        # print_error("Can't find login form for current thread")
        return

    resp = browser.login(username, password)
    # browser.refresh()

    if not browser.find_login_form():
        if login_analysis(browser, url, resp, first_login_form):
            if browser.login_form.entry_text:
                print_found(username, password)
                result.put([url, username, password])
                return True
            else:
                print_found(None, password)
                result.put([url, None, password])
                return True
        browser.session.cookies.clear()
        browser.session.close()

    return False


def send_basic_auth(browser, url, username, password, result):
    printg(f"Username: \033[96m{username:29.29}\033[0m Password: \033[95m{password:29.29}\033[0m")
    resp = browser.open(url, verify=False, auth=(username, password))
    if resp.status_code == 401:
        pass
    elif resp.status_code >= 400:
        print_error(f"\"\033[96m{username}\033[0m\":\"\033[95m{password}\033[0m\"", info=resp.status_code)
    else:
        print_found(username, password)
        result.put([url, username, password])
