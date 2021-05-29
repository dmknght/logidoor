def info(data, name="INFO"):
    print(f"[+] [\033[34m{name}\033[0m] {data}")


def success(data, name="INFO"):
    print(f"[*] [\033[32m{name}\033[0m] [\033[32m{data}\033[0m]")


def error(data, name="ERR"):
    print(f"[\033[31mx\033[0m] [\033[31m{name}\033[0m] {data}")


def warn(data, name="INFO"):
    print(f"[-] [\033[33m{name}\033[0m] {data}")


def fail(account, msg="Invalid", title="", name="FAILED"):
    print(f"[\033[31m-\033[0m] [\033[31m{name}\033[0m] [\033[34m{msg}\033[0m] --> [\033[37m{title}\033[0m] {account}")


def found(user, passwd, title):
    print(f"[\033[37m*\033[0m] [\033[36mMATCH\033[0m] ['\033[32m{user}\033[0m':'\033[32m{passwd}\033[0m']"
          f" [\033[37m{title}\033[0m]")


def vuln(data):
    print(f"[\033[31m*\033[0m] [\033[31m{data}\033[0m]")
