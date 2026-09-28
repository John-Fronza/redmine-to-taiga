from csv_reader import read_csv


rows = read_csv("input/redmine.csv")

print(f"Total de registros: {len(rows)}")

for row in rows[:2]:
    print(row)
    print()