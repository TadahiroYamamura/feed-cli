import csv
import sys


def convert(filepath):
    with open(filepath, mode="r", encoding="cp932") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row["A"], row["C"], row["B"])


if __name__ == "__main__":
    convert(sys.argv[1])
