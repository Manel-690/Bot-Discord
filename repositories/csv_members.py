class MembersRepository:
    """
    Repositório dos membros do clube.
    Lê e escreve no CSV correspondente.
    """
    def __init__(self, path: str = "database/members.csv"):
        self.path = path

    def exists(self, player_id: str = None, phone: str = None) -> bool:
        with open(self.path, mode="r", encoding="utf-8") as arq:
            for linha in arq:
                col = linha.strip().split(",")
                if col[1] == player_id or col[2] == phone:
                    return True
        return False

    def save(self, name: str, player_id: str, phone: str, trophies: int, division_name: str):
        with open(self.path, mode="a", encoding="utf-8") as arq:
            arq.write(",".join([name, player_id, phone, trophies, division_name]) + "\n")