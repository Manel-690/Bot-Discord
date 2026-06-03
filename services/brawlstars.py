import httpx

BRAWL_API_URL = "http://64.181.184.46:3000/v1"

async def get_player_data(game_id: str):
    url = f"{BRAWL_API_URL}/players/{game_id}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao conectar na VPS: {e}")
            return None

async def get_trophies(game_id: str):
    dados = await get_player_data(game_id)
    if dados:
        return int(dados.get("trophies", 0))
    return 0