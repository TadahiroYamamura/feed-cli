import csv
import re
import sys

import master


title_regex = re.compile(r".*【(.*)】")
address_master = master.Address()


def convert(filepath):
    global address_master
    yield [
        "job_id",
        "title",
        "description",
        "analyze_title",
        "analyze_description",
        "image_link",
        "link",
        "job_type",
        "salary",
        "currency",
        "country",
        "prefecture",
        "city",
        "route",
        "zipcode",
    ]
    with open(filepath, mode="r", encoding="cp932") as f:
        for row in csv.DictReader(f):
            job_id = row["お仕事No"]
            title = calc_title(row)
            description = calc_description(row)
            analyze_title = row["都道府県"]
            analyze_description = address_master.get(row["都道府県"]) + "の求人"
            image_link = row["画像ファイル名"]
            link = calc_url(row)
            job_type = "{}-{}".format(row["職種"], row["業種"])
            salary = calc_salary(row["給与"])
            currency = "JPY"
            country = "JP"
            prefecture = address_master.get(row["都道府県"])
            city = row["市区町村"]
            route = row["路線名"]
            yield [
                job_id,
                title,
                description,
                analyze_title,
                analyze_description,
                image_link,
                link,
                job_type,
                salary,
                currency,
                country,
                prefecture,
                city,
                route,
                "",
            ]


def calc_title(row):
    global title_regex
    title_match = title_regex.match(row["メインキャッチ"])
    if (title_match is None):
        return row["メインキャッチ"]
    else:
        return title_match.group(1)


def calc_description(row):
    sp = row["PR文章"].split("\n")
    line = sp[min([len(sp) - 1, 1])]
    sp = line.split("<br>")
    line = sp[min([len(sp) - 1, 1])]
    return line


def calc_url(row):
    return "https://jobpark.works/recruit/detail/{}/".format(row["お仕事ID"])
    return ";".join(ite)


def calc_salary(text):
    return text.split("<br")[0].split("\n")[0]
