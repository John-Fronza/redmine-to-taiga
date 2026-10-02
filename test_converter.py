from converter import convert_csv


issues = convert_csv("input/redmine.csv")

print(f"Total de registros: {len(issues)}")

for issue in issues[:2]:
    print(issue)
    print()