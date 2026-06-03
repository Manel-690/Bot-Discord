class MembersRepository:
    """
    Repositório dos membros do clube.
    Lê e escreve no CSV correspondente.
    """
    def __init__(self, path: str = "database/members.csv"):
        self.path = path

    def exists(self, game_id: str = None, phone: str = None) -> bool:
        with open(self.path, mode="r", encoding="utf-8") as arq:
            for linha in arq:
                col = linha.strip().split(",")
                if col[1] == game_id or col[2] == phone:
                    return True
        return False

    def save(self, name: str, game_id: str, phone: str, trophies: str):
        with open(self.path, mode="a", encoding="utf-8") as arq:
            arq.write(",".join([name, game_id, phone, trophies]) + "\n")