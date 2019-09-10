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
    with open(filepath, mode="r", encoding="cp932") as f:
        reader = csv.DictReader(f)
        for row in reader:
            job_id = row["お仕事No"]
            location_id = row["都道府県"]
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
            yield [
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
            ]


def calc_title(row):
    global title_regex
    title_match = title_regex.match(row["メインキャッチ"])
    if (title_match is None):
        return row["メインキャッチ"]
    else:
        return title_match.group(1)


def calc_subtitle(row):
  global address_master
  return address_master.get(row["都道府県"]) + row["市区町村"]


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


def calc_keyword(row):
    keywords = []
    return ";".join(keywords)


def calc_address(row):
    global address_master
    return ", ".join([row["市区町村"], address_master.get(row["都道府県"]), "日本"])


def calc_similar_id(row):
    similar = []
    return ",".join(similar)


def calc_custom_Parameter(row):
    param = {}
    ite = map(lambda x: "{{_{}}}={}".format(x[0], x[1]), param.items())
    return ";".join(ite)


def calc_salary(text):
    return text.split("<br")[0].split("\n")[0]
