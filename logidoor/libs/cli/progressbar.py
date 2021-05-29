import sys


def printg(text):
    """
    Print text to screen and then delete it (replace by spaces)
    :param text: string = text to screen
    :return: True (dummy)
    """
    if len(text) < 80:
        space = " " * 80
    else:
        space = " " * len(text)
    sys.stdout.write(f"{space}\r")
    sys.stdout.flush()
    sys.stdout.write(f"{text}\r")
    sys.stdout.flush()
