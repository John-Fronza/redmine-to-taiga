from getpass import getpass
from taiga_api import TaigaAPI
from mappings import (
    resolve_status_ids,
    resolve_priority_ids,
    resolve_type_ids,
    resolve_assignee,
)

api = TaigaAPI(
    base_url="http://localhost:9000",
    username=input("Usuário do Taiga: "),
    password=getpass("Senha do Taiga: "),
)

api.authenticate()

project_id = 1

statuses = api.get_issue_statuses(project_id)
priorities = api.get_priorities(project_id)

status_map = resolve_status_ids(statuses)
priority_map = resolve_priority_ids(priorities)

print("\nMapeamento de status:")
for name, status_id in status_map.items():
    print(f"{name} -> {status_id}")

print("\nMapeamento de prioridades:")
for name, priority_id in priority_map.items():
    print(f"{name} -> {priority_id}")

type_map = api.ensure_issue_types(
    project_id=project_id,
    type_names=["infra", "study"],
)

resolved_types = resolve_type_ids(type_map)

print("\nMapeamento de tipos:")
for name, type_id in resolved_types.items():
    print(f"{name} -> {type_id}")

taiga_members = api.get_project_memberships(project_id=project_id)

print("\nMembros do projeto:")
for member in taiga_members:
    print(member)


print("\nTeste de responsáveis:")

test_names = [
    "john.nicolas",
    "Pessoa Inexistente",
    "",
]

for name in test_names:
    user_id = resolve_assignee(name, taiga_members)
    print(f"{name!r} -> {user_id}")


custom_fields = api.get_issue_custom_attributes(project_id)

print("\nCustom Fields do projeto:")

for field in custom_fields:
    print({
        "id": field.get("id"),
        "name": field.get("name"),
        "type": field.get("type"),
        "project": field.get("project"),
        "order": field.get("order"),
    })


custom_field_id = api.ensure_issue_custom_attribute(
    project_id=project_id,
    name="Informações Adicionais",
)

print(f"\nID do campo de informações adicionais: {custom_field_id}")
