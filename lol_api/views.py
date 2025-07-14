import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv
import os

load_dotenv()

# Riot API key and base URL
RIOT_API_KEY= os.getenv('RIOT_API_KEY')
RIOT_BASE_URL = 'https://americas.api.riotgames.com/'

# Helper function to get player data using the new endpoint
def get_player_data(game_name, tag_line):
    # New endpoint to get the PUUID
    account_url = f'{RIOT_BASE_URL}riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}'
    response = requests.get(account_url, headers={'X-Riot-Token': RIOT_API_KEY})
    
    if response.status_code != 200:
        return None
    
    account_data = response.json()
    puuid = account_data['puuid']  # The PUUID is in the 'id' field of the response
    
    # Get the last 10 matches of the player
    matchlist_url = f'{RIOT_BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids'
    matchlist_response = requests.get(matchlist_url, headers={'X-Riot-Token': RIOT_API_KEY})
    
    if matchlist_response.status_code != 200:
        return None
    
    match_ids = matchlist_response.json()[:10]  # Get last 10 match IDs
    
    return puuid, match_ids

def get_champion_data(champion_id):
    # Get champion's info from Riot's API
    champion_url = f'{RIOT_BASE_URL}lol/static-data/v4/champions/{champion_id}'
    response = requests.get(champion_url, headers={'X-Riot-Token': RIOT_API_KEY})
    if response.status_code == 200:
        return response.json()
    return None

@api_view(['GET'])
def get_lol_analytics(request, game_name, tag_line):
    # Fetch the player data using the new account API
    player_data = get_player_data(game_name, tag_line)
    
    if not player_data:
        return JsonResponse({'error': 'Player not found or invalid data'}, status=404)
    
    puuid, match_ids = player_data
    
    kill_participation = 0
    champion_stats = {}
    
    individual_matches=[]

    # Fetch the last 10 matches and calculate average kill participation
    for match_id in match_ids:
        match_url = f'{RIOT_BASE_URL}lol/match/v5/matches/{match_id}'
        match_response = requests.get(match_url, headers={'X-Riot-Token': RIOT_API_KEY})
        
        if match_response.status_code == 200:
            match_data = match_response.json()
            if match_data['info']['gameMode'] == 'CLASSIC':
                for participant in match_data['info']['participants']:
                    if participant['puuid'] == puuid:
                        try:
                            challenges = participant['challenges']
                            kp = challenges['killParticipation']
                            gold_per_minute = challenges['goldPerMinute']
                            kill_participation += kp
                        except KeyError:
                            gold_per_minute = 0
                            kp = 0
                        champion_name = participant['championName']
                        individual_matches.append({champion_name:{ 'kp':kp,'gold_per_minute':gold_per_minute, 'image': f"https://ddragon.leagueoflegends.com/cdn/15.13.1/img/champion/{champion_name}.png"}})
                    
                    
    kill_participation /= len(match_ids)

    
    return JsonResponse({
        'average_kill_participation': kill_participation,
        'matches': individual_matches
    })
