import csv
import re
import sys

import master
import tool


title_regex = re.compile(r".*【(.*)】")
holiday_regex = re.compile(r"年間休日\D*(\d+)\D*", re.MULTILINE)
salary_regex = re.compile(r"[\d,]+")
address_master = master.Address()
condition_master = master.Condition()


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
            title = tool.take(calc_title(row), 20)
            description = tool.take(calc_description(row), 40)
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
    subtitle_elements = []

    # holiday
    global holiday_regex
    holiday_match = holiday_regex.search(row["休日休暇"])
    if (holiday_match is not None):
      holiday_count = holiday_match.group(1)
      if int(holiday_count) > 119:
        subtitle_elements.append('年休'+holiday_count+'日')

    # conditions
    global condition_master
    condition_list = row["条件"].split(',')
    condition_list = filter(lambda x: x, condition_list)
    condition_list = filter(lambda x: int(x) in [7, 12, 11, 8], condition_list)
    condition_list = map(lambda x: condition_master.get(x), condition_list)
    for condition in condition_list:
      subtitle_elements.append(condition)

    # result
    return '、'.join(subtitle_elements)


def calc_url(row):
    return "https://jobpark.works/recruit/detail/{}/?utm_source=line&utm_medium=social&utm_campaign=rt".format(row["お仕事ID"])
    return ";".join(ite)


def calc_salary(text):
    global salary_regex
    salary_text = text.split("<br")[0].split("\n")[0]
    m = salary_regex.search(salary_text)
    if m is None:
        return ''
    else:
        return m[0].replace(",", "")
