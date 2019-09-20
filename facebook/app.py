import csv
import re
import sys

import master


title_regex = re.compile(r".*【(.*)】")
holiday_regex = re.compile(r"年間休日\D*(\d+)\D*", re.MULTILINE)
salary_regex = re.compile(r"[\d,]+")
address_master = master.Address()
condition_master = master.Condition()


def convert(filepath):
    yield [
        "id",
        "title",
        "ios_url",
        "ios_app_store_id",
        "ios_app_name",
        "android_url",
        "android_package",
        "android_app_name",
        "windows_phone_url",
        "windows_phone_app_id",
        "windows_phone_app_name",
        "description",
        "google_product_category",
        "product_type",
        "link",
        "image_link",
        "condition",
        "availability",
        "price",
        "sale_price",
        "sale_price_effective_date",
        "gtin",
        "brand",
        "mpn",
        "item_group_id",
        "gender",
        "age_group",
        "color",
        "size",
        "shipping",
        "custom_label_0",
        "custom_label_1",
        "custom_label_2",
    ]
    with open(filepath, mode="r", encoding="cp932") as f:
        reader = csv.DictReader(f)
        for row in reader:
            job_id = row["お仕事No"]
            location_id = row["都道府県"]
            title = calc_title(row)
            final_url = calc_url(row)
            image_url = row["画像ファイル名"]
            description = calc_description(row)
            salary = calc_salary(row["給与"])
            category = "{}-{}".format(row["職種"], row["業種"])
            address = calc_address(row)
            yield [
                job_id,
                title,
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                description,
                "",
                "",
                final_url,
                image_url,
                "new",
                "available for order",
                salary,
                "",
                "",
                "",
                "ジョブパーク",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                address,
                location_id,
                category,
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
    return "https://jobpark.works/recruit/detail/{}/?utm_source=facebook&utm_medium=social&utm_campaign=rt".format(row["お仕事ID"])


def calc_address(row):
    global address_master
    return ", ".join([row["市区町村"], address_master.get(row["都道府県"]), "日本"])


def calc_salary(text):
    global salary_regex
    salary_text = text.split("<br")[0].split("\n")[0]
    m = salary_regex.search(salary_text)
    if m is None:
        return ''
    else:
        return m[0].replace(",", "") + " JPY"
