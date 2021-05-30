import threading
import queue

from logidoor.libs.browser import Browser
# from logidoor.libs.cli.progressbar import printg
from logidoor.libs.cli.printf import *


def run_threads(threads):
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def setup_threads(browser, url, options, result, target):
    workers = []
    for username in options.userlist:
        for password in options.passlist:
            if len(workers) == options.threads:
                # When login is found, we added URL to queue list
                # We check the URL to detect if login is done
                if url in [check_urls[0] for check_urls in list(result.queue)]:
                    return
                run_threads(workers)
                del workers[:]
            worker = threading.Thread(target=target, args=(browser, url, username, password, result))
            worker.daemon = True
            workers.append(worker)
    if workers:
        run_threads(workers)
        del workers[:]


def setup_threads_no_username(browser, url, options, result, target):
    workers = []
    for password in options.passlist:
        if len(workers) == options.threads:
            # When login is found, we added URL to queue list
            # We check the URL to detect if login is done
            if url in [check_urls[0] for check_urls in list(result.queue)]:
                return
            run_threads(workers)
            del workers[:]
        worker = threading.Thread(target=target, args=(browser, url, None, password, result))
        worker.daemon = True
        workers.append(worker)
    if workers:
        run_threads(workers)
        del workers[:]


def http_attack(url, options, result):
    browser = Browser()
    try:
        from logidoor.modules import http_attack
        resp = browser.open(url)
        target = http_attack.send_form_auth
        if resp.status_code == 401:
            target = http_attack.send_basic_auth
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
