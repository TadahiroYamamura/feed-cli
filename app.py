import sys
from google import app as ggl
from yahoo import app as yh
from facebook import app as fb
from line import app as ln


not_found_message = "The file '{}' not found. Please make sure file exists."


def main():
    if len(sys.argv) < 3:
        return help()
    else:
        try:
            return eval("{}('{}')".format(sys.argv[1], sys.argv[2]))
        except NameError:
            return help()


def google(filepath):
    global not_found_message
    try:
        ggl.convert(filepath)
    except FileNotFoundError:
        print(not_found_message.format(filepath))


def yahoo(filepath):
    global not_found_message
    try:
        yh.convert(filepath)
    except FileNotFoundError:
        print(not_found_message.format(filepath))


def facebook(filepath):
    global not_found_message
    try:
        fb.convert(filepath)
    except FileNotFoundError:
        print(not_found_message.format(filepath))


def line(filepath):
    global not_found_message
    try:
        ln.convert(filepath)
    except FileNotFoundError:
        print(not_found_message.format(filepath))


def help():
    """ ツールの使用方法を表示
    """
    print("usage: app.py target filepath")
    print()
    print("available target")
    print("  - google   : Google Ads")
    print("  - yahoo    : Yahoo")
    print("  - facebook : Facebook")
    print("  - line     : Line")
    print()


if __name__ == "__main__":
    main()
