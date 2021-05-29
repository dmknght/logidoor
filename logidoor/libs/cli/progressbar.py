import sys


def printg(text):
    """
    Print text to screen and then delete it (replace by spaces)
    :param text: string = text to screen
    :return: True (dummy)
    """
    space = " " * 80
    sys.stdout.write(f"{space}\r")
    sys.stdout.flush()
    sys.stdout.write(f"{text}\r")
    sys.stdout.flush()
