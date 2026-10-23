
from getpass import getpass

from taiga_api import TaigaAPI
from converter import convert_csv
from mappings import (
    resolve_status_ids,
    resolve_priority_ids,
    resolve_type_ids,
)
from issue_builder import build_issue


api = TaigaAPI(
    base_url="http://localhost:9000",
    username=input("Usuário do Taiga: "),
    password=getpass("Senha do Taiga: "),
)

api.authenticate()

project_id = 1

# Consulta os dados necessários para preparar a issue.
taiga_members = api.get_project_memberships(project_id)
statuses = api.get_issue_statuses(project_id)
priorities = api.get_priorities(project_id)
type_map = api.ensure_issue_types(project_id, ["infra", "study"])

status_ids = resolve_status_ids(statuses)
priority_ids = resolve_priority_ids(priorities)
type_ids = resolve_type_ids(type_map)

# Converte o CSV e prepara somente a primeira issue.
issues = convert_csv("input/redmine.csv", taiga_members)

result = build_issue(
    converted_issue=issues[0],
    project_id=project_id,
    status_ids=status_ids,
    priority_ids=priority_ids,
    type_ids=type_ids,
)

print("\nIssue que será criada:")
print(result["issue_data"])

confirm = input(
    "\nIsso criará uma issue real no Taiga. "
    "Deseja continuar? Digite CRIAR para confirmar: "
)

if confirm == "CRIAR":
    created_issue = api.create_issue(result["issue_data"])
    custom_attribute_id = api.ensure_issue_custom_attribute(
        project_id,
        "Informações Adicionais",
    )

    api.update_issue_custom_attributes(
        issue_id=created_issue["id"],
        attributes_values={
            str(custom_attribute_id): result["additional_text"],
        },
        version=created_issue["version"],
    )

    print("Informações adicionais salvas com sucesso!")

    print("\nIssue criada com sucesso!")
    print(f"ID: {created_issue['id']}")
    print(f"Título: {created_issue['subject']}")
else:
    print("\nOperação cancelada. Nenhuma issue foi criada.")
