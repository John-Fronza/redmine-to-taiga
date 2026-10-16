
STATUS_MAP = {
    "Aberta": "New",
    "Aprovação": "Ready for test",
    "Fechada": "Closed",
}

PRIORITY_MAP = {
    "Média": "Normal",
    "Alta": "High",
}

TYPE_NAMES = {
    "infra": "infra",
    "study": "study",
}


def build_id_map(items):
    """Transforma uma lista de objetos do Taiga em nome -> ID."""
    return {
        item["name"].lower(): item["id"]
        for item in items
    }


def resolve_status_ids(statuses):
    """Converte os nomes de status do Redmine em IDs do Taiga."""
    taiga_statuses = build_id_map(statuses)

    return {
        redmine_name: taiga_statuses[taiga_name.lower()]
        for redmine_name, taiga_name in STATUS_MAP.items()
    }


def resolve_priority_ids(priorities):
    """Converte os nomes de prioridade do Redmine em IDs do Taiga."""
    taiga_priorities = build_id_map(priorities)

    return {
        redmine_name: taiga_priorities[taiga_name.lower()]
        for redmine_name, taiga_name in PRIORITY_MAP.items()
    }

def resolve_type_ids(type_map):
    """Converte os nomes de tracker do Redmine em IDs de tipos do Taiga."""
    return {
        redmine_name: type_map[taiga_name.lower()]
        for redmine_name, taiga_name in TYPE_NAMES.items()
    }


def resolve_assignee(redmine_name, members):
    """Retorna o ID do usuário correspondente ou None."""
    if not redmine_name or not redmine_name.strip():
        return None

    redmine_name = redmine_name.strip().casefold()

    for member in members:
        taiga_name = member.get("full_name", "")

        if taiga_name.strip().casefold() == redmine_name:
            return member["user"]

    return None
