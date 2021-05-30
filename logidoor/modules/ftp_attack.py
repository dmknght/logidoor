import ftplib
from logidoor.libs.cli.progressbar import printg
from logidoor.libs.cli.printf import *


def send_ftp_auth(session, url, username, password, result):
    try:
        # https://stackoverflow.com/a/51831373
        # ftplib uses host address only. No protocol can be provided
        session.connect(url.split("/")[2])
        printg(f"Username: \033[96m{username:29.29}\033[0m Password: \033[95m{password:29.29}\033[0m")
        session.login(user=username, passwd=password)
        print_found(username, password)
        result.put([url, username, password])

    except ftplib.error_perm:
        pass  # Login failed
    except:
        # Error here better to show
        pass
    finally:
        session.close()


def check_anonymous_login(session, url):
    try:
        # ftplib uses host address only. No protocol can be provided
        session.connect(url.split("/")[2])
        session.login(user="anonymous", passwd="")
        session.close()
        print_warn("Anonymous login is allowed")

    except ftplib.error_perm:
        pass  # Login failed
    except:
        # Error here better to show
        pass
    finally:
        session.close()
