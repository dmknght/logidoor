import queue

from logidoor.libs.browser import Browser
from logidoor.libs.cli.printf import *
from logidoor.libs.thread_controller import setup_threads, setup_threads_no_username


def http_attack(url, options, result):
    browser = Browser()
    try:
        from logidoor.modules import http_attack
        resp = browser.open(url)
        target = http_attack.send_form_auth
        print(resp.status_code)
        if resp.status_code == 401:
            target = http_attack.send_basic_auth
            setup_threads(browser, url, options, result, target=target)
            return
        login_form = browser.find_login_form()
        if login_form:
            browser.login_form = login_form
            if browser.login_form.entry_text:
                # If login form contains both entry_text and entry_password
                if not options.userlist:
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


def ftp_attack(url, options, result):
    if not options.userlist:
        print_error(f"Username is required for FTP protocol")
        return
    from ftplib import FTP
    from logidoor.modules.ftp_attack import send_ftp_auth, check_anonymous_login

    session = FTP()

    check_anonymous_login(session, url)

    target = send_ftp_auth
    setup_threads(session, url, options, result, target)


def do_attack(options):
    result = queue.Queue()

    for url in options.url:
        print_attack(url)
        if url.startswith(("http://", "https")):
            http_attack(url, options, result)
        elif url.startswith("ftp://"):
            ftp_attack(url, options, result)
        else:
            print_error(f"Protocol {url.split('/')[0]} is not supported")

    print_results(list(result.queue))
