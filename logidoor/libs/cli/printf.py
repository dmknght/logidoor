import sys


def __clean():
    sys.stdout.write(" " * 80 + "\r")
    sys.stdout.flush()


def print_found(username, password):
    __clean()
    if username:
        print(f"  [\033[97mFound\033[0m][Username: \033[96m{username}\033[0m Password: \"\033[95m{password}\033[0m\"]")
    else:
        print(f"  [\033[97mFound\033[0m][Password: \"\033[95m{password}\033[0m\"]")


def print_attack(url):
    __clean()
    print(f"Attacking \033[94m{url:65.65}\033[0m")
