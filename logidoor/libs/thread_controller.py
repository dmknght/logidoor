import threading


def is_valid_to_add(url, username, result):
    # When login is found, we added URL and username for current url to queue list
    # We check the URL and username to detect if login is done
    # if url == check_url and username == check_username
    for check_values in list(result.queue):
        if username == check_values[1] and url in check_values:
            return False
    return True


def run_threads(threads):
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def setup_threads(browser, url, options, result, target):
    workers = []
    for username in options.get_user_list():
        for password in options.get_pass_list():
            if len(workers) == options.threads:
                run_threads(workers)
                del workers[:]
            if is_valid_to_add(url, username, result):
                if type(password) == tuple:
                    password = "".join(password)
                worker = threading.Thread(target=target, args=(browser, url, username, password, result))
                worker.daemon = True
                workers.append(worker)

    if workers:
        run_threads(workers)
        del workers[:]


def setup_threads_no_username(browser, url, options, result, target):
    workers = []
    for password in options.pass_list:
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
