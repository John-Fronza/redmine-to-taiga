import csv

def read_csv(file_path):
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        rows = list(reader)
    return rows

