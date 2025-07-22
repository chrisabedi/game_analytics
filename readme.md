# README

### prerequisites
- python3
- redis

you can use apt to install redis (like `sudo apt install redis`) and run the server with 

 ```
 sudo systemctl start redis-server
 ```

## Run server

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

create a `.env` and fill it with pertenent info

```
RIOT_API_KEY=xxxxx
REDIS_HOST='localhost'
REDIS_PORT=6379
``` 
then run
```
python manage.py runserver
```

## CRUD Examples 

### Create
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"game_name": "Babeep", "tag_line": "123"}' \
  http://localhost:8000/api/create

```

### Get
```
curl --header "Content-Type: application/json"    http://localhost:8000/api/get/Babeep/123
```
### Get all
```
curl --header "Content-Type: application/json"    http://localhost:8000/api/get/all
```

### Update
```
curl --header "Content-Type: application/json" \
  --request PUT \
  --data '{"game_name": "Babeep", "tag_line": "123"}' \
  http://localhost:8000/api/update
```

### Delete
```
curl -X "DELETE" http://localhost:8000/api/delete/Babeep/123
```


