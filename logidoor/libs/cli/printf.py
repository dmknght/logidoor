import sys


def found(username, password):
    sys.stdout.write(" " * 80 + "\r")
    sys.stdout.flush()
    if username:
        print(f"  [\033[97mFound\033[0m][Username: \033[96m{username}\033[0m Password: \"\033[95m{password}\033[0m\"]")
    else:
        print(f"  [\033[97mFound\033[0m][Password: \"\033[95m{password}\033[0m\"]")
