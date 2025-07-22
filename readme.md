# README

### prerequisites
 python
 redis

 you can use apt to install redis ( like sudo apt install redis)
 and run the server with 

 ```
 sudo systemctl start redis-server```

## Run server

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

create a .env and fill it with pertenent info

```
RIOT_API_KEY=xxxxx
REDIS_HOST='localhost'
REDIS_PORT=6379

```
then 
```
python manage.py runserver
```

## Add CRUD Examples 

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"game_name": "Babeep", "tag_line": "123"}' \
  http://localhost:8000/api/create

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"game_name": "Lsdreama", "tag_line": "NA1"}' \
  http://localhost:8000/api/create

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"game_name": "Henry M0rgan", "tag_line": "NA1"}' \
  http://localhost:8000/api/create

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"game_name": "Bilbro Swaggins", "tag_line": "6836"}' \
  http://localhost:8000/api/create

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"game_name": "Cote", "tag_line": "NA1"}' \
  http://localhost:8000/api/create

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"game_name": "Que Rico", "tag_line": "NA1"}' \
  http://localhost:8000/api/create

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"game_name": "Peraza", "tag_line": "yeet"}' \
  http://localhost:8000/api/create
```

## Get one Player Info
```
curl --header "Content-Type: application/json"    http://localhost:8000/api/get/Babeep/123
```
## Get all Player key/values
```
curl --header "Content-Type: application/json"    http://localhost:8000/api/get/all
```

## Remove a player from tracking
```
curl -X "DELETE" http://localhost:8000/api/delete/Babeep/123
```

## Update a players info
```
curl --header "Content-Type: application/json" \
  --request PUT \
  --data '{"game_name": "Babeep", "tag_line": "123"}' \
  http://localhost:8000/api/update
```

