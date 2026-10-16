
from csv_reader import read_csv

file_path = "input/redmine.csv"
issues = read_csv(file_path)

statuses = set()
priorities = set()

for issue in issues:
    if issue["Status"].strip():
        statuses.add(issue["Status"].strip())

    if issue["Priority"].strip():
        priorities.add(issue["Priority"].strip())

print("Status encontrados no Redmine:")
for status in sorted(statuses):
    print(f"- {status}")

print("\nPrioridades encontradas no Redmine:")
for priority in sorted(priorities):
    print(f"- {priority}")

print(f"\nTotal de issues analisados: {len(issues)}")