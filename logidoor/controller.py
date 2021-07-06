import queue

from logidoor.libs.browser import Browser
from logidoor.libs.cli.printf import *
from logidoor.libs.thread_controller import setup_threads, setup_threads_no_username


def http_attack(url, options, result):
    browser = Browser()
    try:
        from logidoor.modules import http_attack
        resp = browser.open(url, verify=False)

        # browser.first_page = browser.page
        # try:
        #     browser.first_title = browser.page.title.text
        # except AttributeError:
        #     browser.first_title = None
        # browser.first_content = convert.handle(resp.text)
        target = http_attack.send_form_auth

        if resp.status_code == 401:
            target = http_attack.send_basic_auth
            setup_threads(browser, url, options, result, target=target)
            return
        login_form = browser.find_login_form()
        if login_form:
            browser.login_form = login_form
            if browser.login_form.entry_text:
                # If login form contains both entry_text and entry_password
                if not options.user_list:
                    print_error(f"Username is required for current URL")
                else:
                    setup_threads(browser, url, options, result, target=target)
            else:
                # Only password, we setup different
                setup_threads_no_username(browser, url, options, result, target)
        else:
            print_no_login_found(url)
    except KeyboardInterrupt:
        exit(0)
    finally:
        browser.close()


def do_attack(options):
    result = queue.Queue()
    for url in options.url:
        print_attack(url)
        if url.startswith(("http://", "https")):
            http_attack(url, options, result)
        else:
            print_error(f"Protocol {url.split('/')[0]} is not supported")

    print_results(list(result.queue))
