
def build_additional_text(additional_data):
    """Organiza os dados extras do Redmine em um texto legível."""
    lines = []

    for field, value in additional_data.items():
        if value is not None and value != "":
            label = field.replace("_", " ").capitalize()
            lines.append(f"{label}: {value}")

    return "\n".join(lines)


def build_issue(
    converted_issue,
    project_id,
    status_ids,
    priority_ids,
    type_ids,
):
    """Prepara os dados de uma issue para a API do Taiga."""
    taiga_data = converted_issue["taiga_data"]
    additional_data = converted_issue["additional_data"]

    status_name = taiga_data["status"]
    priority_name = taiga_data["priority"]
    type_name = taiga_data["tracker"]

    issue_data = {
        "project": project_id,
        "subject": taiga_data["subject"],
        "description": taiga_data["description"] or "",
        "status": status_ids[status_name],
        "priority": priority_ids[priority_name],
        "type": type_ids[type_name],
        "assigned_to": taiga_data["assignee"],
        "due_date": taiga_data["due_date"],
    }

    additional_text = build_additional_text(additional_data)

    if taiga_data["last_notes"]:
        additional_text += (
            "\n\nÚltimas anotações:\n"
            + taiga_data["last_notes"]
        )

    return {
        "issue_data": issue_data,
        "additional_text": additional_text,
    }
