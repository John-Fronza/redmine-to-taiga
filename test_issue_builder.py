
from getpass import getpass

from converter import convert_csv
from mappings import (
    resolve_status_ids,
    resolve_priority_ids,
    resolve_type_ids,
)
from taiga_api import TaigaAPI
from issue_builder import build_issue


api = TaigaAPI(
    base_url="http://localhost:9000",
    username=input("Usuário do Taiga: "),
    password=getpass("Senha do Taiga: "),
)

api.authenticate()

project_id = 1

# Consulta as configurações atuais do projeto.
taiga_members = api.get_project_memberships(project_id)
statuses = api.get_issue_statuses(project_id)
priorities = api.get_priorities(project_id)

# Garante que os tipos necessários existam.
type_map = api.ensure_issue_types(project_id, ["infra", "study"])

# Converte os nomes em IDs do Taiga.
status_ids = resolve_status_ids(statuses)
priority_ids = resolve_priority_ids(priorities)
type_ids = resolve_type_ids(type_map)

# Lê o CSV e converte os registros do Redmine.
issues = convert_csv("input/redmine.csv", taiga_members)

print(f"\nTotal de registros convertidos: {len(issues)}")

# Prepara apenas a primeira issue, sem enviá-la à API.
result = build_issue(
    converted_issue=issues[0],
    project_id=project_id,
    status_ids=status_ids,
    priority_ids=priority_ids,
    type_ids=type_ids,
)

print("\n--- Dados preparados para a issue ---")
print(result["issue_data"])

print("\n--- Informações adicionais ---")
print(result["additional_text"])
