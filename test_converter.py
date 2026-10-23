
from getpass import getpass

from converter import convert_csv
from taiga_api import TaigaAPI


api = TaigaAPI(
    base_url="http://localhost:9000",
    username=input("Usuário do Taiga: "),
    password=getpass("Senha do Taiga: "),
)

api.authenticate()

project_id = 1
taiga_members = api.get_project_memberships(project_id)

issues = convert_csv("input/redmine.csv", taiga_members)

print(f"\nTotal de registros: {len(issues)}")

for issue in issues[:5]:
    taiga_data = issue["taiga_data"]
    additional_data = issue["additional_data"]

    print(f"\nRedmine ID: {additional_data['redmine_id']}")
    print(f"Assunto: {taiga_data['subject']}")
    print(f"Status original: {taiga_data['status']}")
    print(f"Prioridade original: {taiga_data['priority']}")
    print(f"Tipo original: {taiga_data['tracker']}")
    print(f"Responsável Taiga: {taiga_data['assignee']}")
    print(
        "Responsável original não encontrado: "
        f"{additional_data.get('redmine_assignee', 'Não se aplica')}"
    )
    print(f"Prazo: {taiga_data['due_date']}")
