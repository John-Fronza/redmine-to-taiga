
import requests


class TaigaAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.token = None

    def authenticate(self):
        url = f"{self.base_url}/api/v1/auth"

        response = requests.post(
            url,
            json={
                "type": "normal",
                "username": self.username,
                "password": self.password,
            },
            timeout=15,
        )
        response.raise_for_status()

        self.token = response.json()["auth_token"]
        return self.token

    def get(self, endpoint, params=None):
        if not self.token:
            raise RuntimeError("Autentique-se antes de consultar a API.")

        url = f"{self.base_url}/api/v1/{endpoint.lstrip('/')}"

        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.token}"},
            params=params,
            timeout=15,
        )
        response.raise_for_status()

        return response.json()

    def get_issue_types(self, project_id):
        return self.get(
            "issue-types",
            params={"project": project_id},
        )
    
    def ensure_issue_types(self, project_id, type_names):
        existing_types = self.get_issue_types(project_id)

        # Guarda o nome de cada tipo e seu ID
        type_map = {
            issue_type["name"].lower(): issue_type["id"]
            for issue_type in existing_types
        }

        # Descobre a próxima posição na lista
        next_order = max(
            (issue_type["order"] for issue_type in existing_types),
            default=0,
        ) + 1

        for name in type_names:
            if name.lower() in type_map:
                print(f"Tipo '{name}' já existe.")
                continue

            url = f"{self.base_url}/api/v1/issue-types"

            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.token}",
                },
                json={
                    "name": name,
                    "order": next_order,
                    "color": "#5178D3",
                    "project": project_id,
                },
                timeout=15,
            )
            response.raise_for_status()

            created_type = response.json()
            type_map[created_type["name"].lower()] = created_type["id"]

            print(f"Tipo '{name}' criado com ID {created_type['id']}.")
            next_order += 1
        return type_map

    
    def get_issue_statuses(self, project_id):
        return self.get(
            "issue-statuses",
            params={"project": project_id},
        )

    def get_priorities(self, project_id):
        return self.get(
            "priorities",
            params={"project": project_id},
        )

    def get_project_memberships(self, project_id):
        """Consulta os membros associados a um projeto."""
        return self.get(
            "memberships",
            params={"project": project_id},
        )
