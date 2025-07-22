import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv
import os
from django.http import JsonResponse
import json
from .utils import redis_client

load_dotenv()


# Riot API key and base URL
RIOT_API_KEY = os.getenv('RIOT_API_KEY')
RIOT_BASE_URL = 'https://americas.api.riotgames.com/'


def get_puuid(game_name, tag_line):
    account_url = f'{RIOT_BASE_URL}riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}'
    response = requests.get(account_url, headers={'X-Riot-Token': RIOT_API_KEY})
    
    if response.status_code != 200:
        return None
    
    account_data = response.json()
    puuid = account_data['puuid']
    return puuid


def get_player_data(game_name, tag_line):

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


def get_rank_tier(puuid):
    
    info_url=f'https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}'
    info_response = requests.get(info_url, headers={'X-Riot-Token': RIOT_API_KEY})
    
    player_info= {}
    if info_response.status_code == 200:
   
        info_data=info_response.json()
        for data in info_data:
            if data["queueType"] == 'RANKED_SOLO_5x5':
                player_info['tier']=data["tier"]
                player_info['rank']=data["rank"]
                player_info['wins'] =data["wins"]
                player_info['losses']=data["losses"]
                player_info['leaguePoints']=data['leaguePoints']
                                                   
    return player_info

    
@api_view(["POST"])
def create_player_info(request):
    data = json.loads(request.body)
    game_name = data.get("game_name")
    tag_line = data.get("tag_line")
    if not game_name and tag_line:
        return JsonResponse({"error": "game_name and tag_line is required"}, status=400)
    
    puuid = get_puuid(game_name, tag_line)
    if not puuid:
        return JsonResponse({"error": "error getting puuid"}, status=400)
    
    player_info = get_rank_tier(puuid)
    redis_client.set(f"{game_name}#{tag_line}",json.dumps(player_info))
    return JsonResponse({"message": "player created", f"{game_name}#{tag_line}": player_info})


@api_view(["GET"])
def get_player_info(request, game_name, tag_line):
    player_info = redis_client.get(f"{game_name}#{tag_line}")
    if not player_info:
        return JsonResponse({"error": "player not found"}, status=404)
    return JsonResponse(json.loads(player_info))


@api_view(["PUT"])
def update_player(request):
    data = json.loads(request.body)
    game_name = data.get("game_name")
    tag_line = data.get("tag_line")
    if not game_name and tag_line:
        return JsonResponse({"error": "game_name and tag_line is required"}, status=400)
    
    if not redis_client.exists(f"{game_name}#{tag_line}"):
        return JsonResponse({"error": "player not found"}, status=404)
    
    puuid = get_puuid(game_name, tag_line)
    if not puuid:
        return JsonResponse({"error": "error getting puuid"}, status=400)
    
    player_info = get_rank_tier(puuid)
    redis_client.set(f"{game_name}#{tag_line}",json.dumps(player_info))
    return JsonResponse({"message": "player updated", f"{game_name}#{tag_line}": player_info})

@api_view(['DELETE'])
def delete_player(request, game_name, tag_line):
    result = redis_client.delete(f"{game_name}#{tag_line}")
    if result == 0:
        return JsonResponse({"error": "player not found"}, status=404)
    return JsonResponse({"message": "player deleted"})

@api_view(['GET'])
def get_all_players(request):
    redis_keys = redis_client.keys()
    players ={}
    for key in redis_keys:
        players[f'{key}']= json.loads(redis_client.get(key))
    return JsonResponse(players)