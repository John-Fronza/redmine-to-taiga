from datetime import datetime

from csv_reader import read_csv
from mappings import resolve_assignee



def clean_text(value):
    if not value:
        return None

    value = value.strip()

    return value if value else None


def convert_int(value):
    value = clean_text(value)

    if value is None:
        return None

    return int(value)


def convert_float(value):
    value = clean_text(value)

    if value is None:
        return None

    return float(value)


def convert_bool(value):
    value = clean_text(value)

    if value is None:
        return None

    return value.lower() == "yes"


def convert_date(value):
    value = clean_text(value)

    if value is None:
        return None

    date = datetime.strptime(value, "%d %B %Y")

    return date.strftime("%Y-%m-%d")


def convert_datetime(value):
    value = clean_text(value)

    if value is None:
        return None

    date = datetime.strptime(value, "%d %B %Y %H:%M")

    return date.strftime("%Y-%m-%d %H:%M:%S")


def convert_issue(issue, members):
    """
    Converte uma issue do Redmine para o nosso modelo intermediário.

    Os dados são separados em:

    - taiga_data: informações que pretendemos migrar para o Taiga.
    - additional_data: informações que queremos preservar,
      mas que não serão necessariamente enviadas para o Taiga.
    """

    redmine_assignee = clean_text(issue["Assignee"])
    assignee_id = resolve_assignee(redmine_assignee, members)

    taiga_data = {

        # Informações que serão utilizadas para criar
        # a User Story no Taiga.
        "subject": clean_text(issue["Subject"]),
        "description": clean_text(issue["Description"]),

        # Esses campos ainda precisarão ser mapeados
        # para os IDs correspondentes do Taiga.
        "status": clean_text(issue["Status"]),
        "priority": clean_text(issue["Priority"]),
        "assignee": assignee_id,
        "tracker": clean_text(issue["Tracker"]),

        # Datas que pretendemos avaliar para migração.
        "start_date": convert_date(issue["Start date"]),
        "due_date": convert_date(issue["Due date"]),

        #Gostaria de manter mas não é claro se da pra converter
        "last_notes": clean_text(issue["Last notes"]),
    }

    additional_data = {
        # Identificação da issue original.
        # Será importante para rastrear a migração.
        "redmine_id": convert_int(issue["#"]),

        # Mudanças
        "story_points": convert_float(issue["Storie Points"]),
        # Projeto de origem
        "project": clean_text(issue["Project"]),

        # Possivel conversão porém desnecessario
        "estimated_time": convert_float(issue["Estimated time"]),
        "total_estimated_time": convert_float(issue["Total estimated time"]),
        "spent_time": convert_float(issue["Spent time"]),
        "total_spent_time": convert_float(issue["Total spent time"]),

        "done_percent": convert_int(issue["% Done"]),

        # Hierarquia original.
        "parent_id": convert_int(issue["Parent task"]),
        "parent_subject": clean_text(issue["Parent task subject"]),

        # Informações de autoria e histórico.
        "author": clean_text(issue["Author"]),
        "updated": convert_datetime(issue["Updated"]),
        "created": convert_datetime(issue["Created"]),
        "closed": convert_datetime(issue["Closed"]),
        "last_updated_by": clean_text(issue["Last updated by"]),

        # Informações adicionais do Redmine.
        "category": clean_text(issue["Category"]),
        "target_version": clean_text(issue["Target version"]),

        # Relacionamentos e anexos.
        "related_issues": clean_text(issue["Related issues"]),
        "files": clean_text(issue["Files"]),

        # Campo separado do Description.
        "story_description": clean_text(issue["Storie Description"]),

        # Tester original.
        "tester": clean_text(issue["Tester"]),

        # Visibilidade original.
        "private": convert_bool(issue["Private"]),
    }

    if redmine_assignee and assignee_id is None:
        additional_data["redmine_assignee"] = redmine_assignee

    return {
        "taiga_data": taiga_data,
        "additional_data": additional_data,
    }


def convert_csv(file_path, members):
    issues = read_csv(file_path)

    converted_issues = []

    for issue in issues:
        converted_issue = convert_issue(issue, members)
        converted_issues.append(converted_issue)

    return converted_issues
