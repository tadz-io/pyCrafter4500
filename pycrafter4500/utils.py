from math import floor


def conv_len(a, l):
    """
    Function that converts a number into a bit string of given length.

    :param int a: Number to convert.
    :param int l: Length of bit string.

    :return: Padded bit string.
    """
    b = bin(a)[2:]
    padding = l - len(b)
    b = "0" * padding + b
    return b


def bits_to_bytes(a, reverse=True):
    """
    Function that converts bit string into a given number of bytes.

    :param str a: Bytes to convert.
    :param bool reverse: Whether or not to reverse the byte list.

    :return: List of bytes.
    """
    bytelist = []

    # check if needs padding
    if len(a) % 8 != 0:
        padding = 8 - len(a) % 8
        a = "0" * padding + a

    # convert to bytes
    for i in range(len(a) // 8):
        bytelist.append(int(a[8 * i : 8 * (i + 1)], 2))

    if reverse:
        bytelist.reverse()
    return bytelist


def fps_to_period(fps):
    """
    Calculates desired period (us) from given fps.

    :param int fps: Frames per second.

    :return: Period (us).
    """
    period = int(floor(1.0 / fps * 10**6))
    return period
