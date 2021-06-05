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


def print_error(text, info="INFO"):
    __clean()
    print(f"  [\033[91m{info}\033[0m] {text}")


def print_warn(text):
    __clean()
    print(f"  [\033[93mWARN\033[0m] {text}")


def print_attack(url):
    __clean()
    print(f"Attacking \033[94m{url:65.65}\033[0m")


def print_no_login_found(url):
    __clean()
    print(f"  [\033[91mATT\033[0m] Can't find login at \033[94m{url}\033[0m")


def print_info(text, info="INFO"):
    __clean()
    print(f"  [\033[97m{info}\033[0m] {text}")


def print_results(results):
    __clean()
    if not results:
        print("\nResult: \033[91mNo login found\033[0m")
    else:
        print(f"\nResult: \033[97mFound {len(results)}\033[0m")
        print("-" * 80)
        for result in results:
            url, username, password = result
            print(f"URL: \033[94m{url}\033[0m")
            if username:
                print(f"Username: \"\033[96m{username}\033[0m\"")
            print(f"Password: \"\033[95m{password}\033[0m\"")
            print("-" * 80)
