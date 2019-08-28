import csv


class Condition():
    def __init__(self):
        with open("master/condition.csv", mode="r", encoding="utf-8") as f:
            self.master = {}
            for row in csv.DictReader(f):
                self.master[row["id"]] = row["name"]

    def get(self, condition_id):
        return self.master[condition_id]
