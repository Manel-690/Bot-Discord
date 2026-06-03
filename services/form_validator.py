class FormValidator:
    """
    Serviço de validação do formulário de recrutamento
    """
    def clean(self, player_id: str, phone: str) -> (str, str):
        """
        Limpa e formata os dados de ID e telefone enviados no formulário.

        Parameters
        ----------
        player_id : str
            ID do jogador.
        phone_id : str
            Número de telefone.
        
        Returns
        -------
        str 
            ID em maiúsculo e sem #, caso tenha.
        str
            Apenas os dígitos do número de telefone.
        """
        if player_id.startswith("#"):
            player_id = player_id[1:]
        player_id = player_id.upper()
        phone = "".join(char for char in phone if char.isdigit())

        return player_id, phone

    def validate(self, phone: str) -> str:
        """
        Valida o número de telefone.

        Parameters
        ----------
        phone : str
            Número de telefone.

        Returns
        -------
        str
            Mensagem de erro ou string vazia.
        """
        if len(phone) != 11:
            return "O telefone deve conter 8 dígitos: DDD + 9 + NUM"
        return ""