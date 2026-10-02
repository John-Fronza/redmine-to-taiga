from csv_reader import read_csv


def convert_issue(issue):
    converted = {
        "redmine_id": int(issue["#"]),
        "project": issue["Project"],
        "tracker": issue["Tracker"],
        "subject": issue["Subject"],
        "description": issue["Description"],
        "status": issue["Status"],
        "priority": issue["Priority"],
        "author": issue["Author"],
        "assignee": issue["Assignee"],
        "start_date": issue["Start date"],
        "due_date": issue["Due date"],
        "estimated_time": float(issue["Estimated time"]) if issue["Estimated time"] else None,
        "spent_time": float(issue["Spent time"]) if issue["Spent time"] else None,
        "done_percent": int(issue["% Done"]) if issue["% Done"] else None,
        "story_points": float(issue["Storie Points"]) if issue["Storie Points"] else None,
        "private": issue["Private"].lower() == "yes",
        "last_notes": issue["Last notes"]
    }

    return converted


def convert_csv(file_path):
    issues = read_csv(file_path)

    converted_issues = []

    for issue in issues:
        converted_issue = convert_issue(issue)
        converted_issues.append(converted_issue)

    return converted_issues