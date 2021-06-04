# import random
#
#
# def rand_from_list(arg_list):
#     """
#     Select element in list randomly
#     :param arg_list: a list of values
#     :return: Random element in arg_list
#     """
#     return random.choice(arg_list)
#
#
# def rand_from_file(file_location):
#     """
#     Select a line in a file randomly
#     :param file_location: string = file location
#     :return: a line in the file
#     """
#     return rand_from_list(file_read(file_location).split("\n"))


# def str_to_list(username):
#     """
#     Split input string by ':' value (use for username in options)
#     :param username: string = option users give from keyboard
#     :return: a list of username splits by ':'
#     """
#     return username.split(":")
_version_ = "0.0.1"


def read_lines(file_path):
    """
    Read lines from file as iterator
    :param file_path: string: path to file
    :return:
    """
    f = None
    try:
        f = open(file_path)
        for line in f:
            yield line.replace("\n", "")
    except Exception:
        raise Exception("Error while reading wordlist of password")
    finally:
        if f:
            f.close()

def file_load(file_location):
    """
    Try open a file and give user file object
    :param file_location: string = location of the file
    :return: file object = open(file)
    """
    try:
        file_object = open(file_location, 'r')
        return file_object
    except Exception as error:
        raise Exception(error)


def file_read(file_location):
    """
    Try open file and read all data
    :param file_location: string = path to the file
    :return: string = text in the file
    """
    try:
        file_object = open(file_location, 'r')
        result = file_object.read()
        file_object.close()
        return result
    except Exception as error:
        raise Exception(error)


def file_write(file_location, data):
    """
    Write text to file
    :param file_location: string = path to file
    :param data: string = text to write into file
    :return: None
    """
    try:
        file_object = open(file_location, "w")
        file_object.write(data)
        file_object.close()
    except Exception as error:
        raise Exception(error)


def file_write_append(file_location, data):
    """
    Write data to a file in next line
    :param file_location: string = file location
    :param data: string = text to write
    :return: True
    """
    try:
        file_object = open(file_location, "a")
        file_object.write(data)
        file_object.close()
    except Exception as error:
        raise Exception(error)


# def rand_string(len_min=2, len_max=5, select_type="char"):
#     """
#     Generate a string randomly with random length
#     :param len_min: int[default] = 2 Min value of int range to choose randomly for text len
#     :param len_max: int[default] = 5 Max value of int range to choose randomly for text len
#     :param select_type: string = [ "char" | "dig" ] choose charset type
#     :return: random string
#     refer: https://stackoverflow.com/a/2257449
#     """
#     import string
#
#     # Generate charset range from select_type
#     charset = string.ascii_letters
#     if select_type == "dig":
#         charset = string.digits
#
#     # Generate length of string from len_min and len_max
#     len_min, len_max = 0, random.randint(len_min, len_max)
#
#     # return string value
#     return ''.join(random.choice(charset) for _ in range(len_min, len_max))


def get_domain(url):
    return url.split("/")[2]
