import csv


class Address():
    def __init__(self):
        with open("master/address.csv", mode="r", encoding="utf-8") as f:
            self.master = {}
            for row in csv.DictReader(f):
                self.master[row["id"]] = row["name"]

    def get(self, address_id):
        return self.master[address_id]
