import csv
from ftplib import FTP
import sys
import os

from dotenv import load_dotenv

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
            download_file(sys.argv[2], 'temp')
            converted_file = eval("{}('{}')".format(sys.argv[1], 'temp'))
            upload_file(converted_file, '/japan_data_vision/{}'.format(converted_file))
        except NameError:
            return help()
        finally:
            if os.path.exists(converted_file):
                os.remove(converted_file)
            if os.path.exists('temp'):
                os.remove('temp')


def download_file(ftp_path, download_path):
    load_dotenv()
    ftp = FTP(os.getenv('FTP_HOST'), os.getenv('FTP_USER'), passwd=os.getenv('FTP_PSWD'))
    with open(download_path, 'wb') as w:
        ftp.retrbinary('RETR {}'.format(ftp_path), w.write)


def upload_file(local_path, ftp_path):
    load_dotenv()
    ftp = FTP(os.getenv('FTP_HOST'), os.getenv('FTP_USER'), passwd=os.getenv('FTP_PSWD'))
    with open(local_path, 'rb') as r:
        ftp.storbinary('STOR {}'.format(ftp_path), r)


def google(filepath):
    global not_found_message
    try:
        filename = 'feeddata_google.csv'
        with open(filename, 'w', encoding='utf-8', newline='') as w:
            csv.writer(w).writerows(ggl.convert(filepath))
        return filename
    except FileNotFoundError:
        print(not_found_message.format(filepath))


def yahoo(filepath):
    global not_found_message
    try:
        filename = 'feeddata_yahoo.tsv'
        with open(filename, 'w', encoding='utf-8', newline='') as w:
            csv.writer(w, delimiter='\t').writerows(yh.convert(filepath))
        return filename
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
    print("usage: app.py target ftppath")
    print()
    print("available target")
    print("  - google   : Google Ads")
    print("  - yahoo    : Yahoo")
    print("  - facebook : Facebook")
    print("  - line     : Line")
    print()


if __name__ == "__main__":
    main()
