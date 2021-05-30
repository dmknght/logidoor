import threading


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
