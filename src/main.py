import requests
import json

# Definindo a URL da API
url = "https://blaze1.space/api/roulette_games/history"

# Parâmetros da consulta inicial
params = {
    "startDate": "2024-06-01T20:00:00.000Z",
    "endDate": "2024-06-01T20:00:00.000Z",
    "page": 1
}

# Função para obter os detalhes das apostas por ID de jogo
def get_bet_details(game_id):
    bet_details = []
    page = 1
    
    # Loop para percorrer todas as páginas dos detalhes das apostas
    while True:
        details_url = f"https://blaze1.space/api/roulette_games/{game_id}?page={page}"
        response = requests.get(details_url)
        data = response.json()
        
        # Adicionando as apostas da página aos detalhes
        bet_details.extend(data['bets'])
        
        # Verificando se há mais páginas de detalhes para a aposta
        if page >= data['totalBetPages']:
            break
        
        # Indo para a próxima página de detalhes
        page += 1
    
    return bet_details

# Função principal para obter os dados da API
def main():
    game_details = []
    bet_details = []
    
    # Loop para percorrer todas as páginas da consulta inicial
    page = 1
    while True:
        params['page'] = page
        print(f"Requesting page {page}")
        response = requests.get(url, params=params)
        data = response.json()

        # Iterando sobre os registros retornados
        for record in data['records']:
            game_id = record['id']
            print(f"Processing game_id {game_id}")
            bet_detail = get_bet_details(game_id)
            
            # Adicionando detalhes do jogo à lista
            game_details.append({
                "game_id": game_id,
                "created_at": record['created_at'],
                "color": record['color'],
                "roll": record['roll']
            })
            
            # Adicionando detalhes da aposta à lista
            for bet in bet_detail:
                bet_details.append({
                    "game_id": game_id,
                    "bet": bet
                })
        
        # Verificando se há mais páginas na consulta inicial
        if page >= data['total_pages']:
            break
        
        # Indo para a próxima página da consulta inicial
        page += 1
    
    print(f"Total game records collected: {len(game_details)}")
    print(f"Total bet records collected: {len(bet_details)}")
    return game_details, bet_details

if __name__ == "__main__":
    game_details, bet_details = main()
    
    # Salvando os detalhes do jogo em um arquivo JSON
    with open('../data/game_details.json', 'w') as f:
        json.dump(game_details, f, indent=4)
    print("Game details saved to game_details.json")
    
    # Salvando os detalhes da aposta em um arquivo JSON
    with open('../data/bet_details.json', 'w') as f:
        json.dump(bet_details, f, indent=4)
    print("Bet details saved to bet_details.json")
