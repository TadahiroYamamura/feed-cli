import csv
import re
import sys

import master


title_regex = re.compile(r".*【(.*)】")
holiday_regex = re.compile(r"年間休日\D*(\d+)\D*", re.MULTILINE)
address_master = master.Address()
condition_master = master.Condition()


def convert(filepath):
    yield [
        "Item ID",
        "Item Name",
        "Description",
        "Destination URL",
        "Image URL",
        "Category ID",
        "Formatted Price",
        "Landing Page URL",
        "Smartphone Destination URL",
        "Smartphone Landing Page URL",
        "In Stock",
        "Capacity",
        "Price",
        "Sale Price",
        "Formatted Sale Price",
        "Rating",
        "Reviews",
        "Badge",
        "Display Settings",
    ]
    with open(filepath, mode="r", encoding="cp932") as f:
        reader = csv.DictReader(f)
        for row in reader:
            job_id = row["お仕事No"]
            title = calc_title(row)
            description = calc_description(row)
            final_url = calc_url(row)
            image_url = row["画像ファイル名"]
            category = ''
            salary = calc_salary(row["給与"])
            yield [
                job_id,
                title,
                description,
                final_url,
                image_url,
                category,
                salary,
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
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
    return "https://jobpark.works/recruit/detail/{}/".format(row["お仕事ID"])


def calc_salary(text):
    return text.split("<br")[0].split("\n")[0]
