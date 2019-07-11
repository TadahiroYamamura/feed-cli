import csv
import re
import sys

import master


headers = [
    "Job ID",
    "Location ID",
    "Title",
    "Final URL",
    "Final mobile URL",
    "Image URL",
    "Subtitle",
    "Description",
    "Salary",
    "Category",
    "Contextual keywords",
    "Address",
    "Similar Job IDs",
    "Tracking template",
    "Custom parameter",
]
title_regex = re.compile(r".*【(.*)】")


def convert(filepath):
    print(",".join(headers))
    with open(filepath, mode="r", encoding="cp932") as f:
        reader = csv.DictReader(f)
        for row in reader:
            job_id = row["お仕事No"]
            location_id = row["検索用　都道府県"]
            title = calc_title(row)
            final_url = calc_url(row)
            final_mobile_url = ""
            image_url = row["画像ファイル名"]
            sub_title = calc_subtitle(row)
            description = calc_description(row)
            salary = calc_salary(row["給与"])
            category = "{}-{}".format(row["職種"], row["業種"])
            keyword = calc_keyword(row)
            address = calc_address(row)
            similar_id = calc_similar_id(row)
            tracking_template = ""
            custom_parameter = calc_custom_Parameter(row)
            print("\"" + "\",\"".join([
                job_id,
                location_id,
                title,
                final_url,
                final_mobile_url,
                image_url,
                sub_title,
                description,
                salary,
                category,
                keyword,
                address,
                similar_id,
                tracking_template,
                custom_parameter,
            ]) + "\"")


def calc_title(row):
    global title_regex
    title_match = title_regex.match(row["メインキャッチ"])
    if (title_match is None):
        return row["メインキャッチ"]
    else:
        return title_match.group(1)


def calc_subtitle(row):
    return row["サブキャッチ"].split("\n")[0]


def calc_description(row):
    sp = row["PR文章"].split("\n")
    line = sp[min([len(sp) - 1, 1])]
    sp = line.split("<br>")
    line = sp[min([len(sp) - 1, 1])]
    return line


def calc_url(row):
    return "https://jobpark.works/recruit/detail/{}/".format(row["お仕事ID"])


def calc_keyword(row):
    keywords = []
    return ";".join(keywords)


def calc_address(row):
    return ", ".join([row["市区町村"], master.Address.get(row["検索用　都道府県"]), "日本"])


def calc_similar_id(row):
    similar = []
    return ",".join(similar)


def calc_custom_Parameter(row):
    param = {}
    ite = map(lambda x: "{{_{}}}={}".format(x[0], x[1]), param.items())
    return ";".join(ite)


def calc_salary(text):
    return text.split("<br")[0].split("\n")[0]


if __name__ == "__main__":
    convert(sys.argv[1])
