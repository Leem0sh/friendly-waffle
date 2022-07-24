# Friendly-waffle

### How to use it

1. `git clone https://github.com/Leem0sh/friendly-waffle.git`
2. `docker build -t friendly-waffle:latest friendly-waffle`
3. `docker-compose -f friendly-waffle/docker-compose.yaml up -d`
4. `docker container ls` and find the `applift-api` `<CONTAINER ID>`
5. `docker exec -it <CONTAINER ID> python manage.py migrate`
6. visit `http://localhost:8000/api/applift/docs`
7. enjoy

### Secrets - create .env file

    SECRET_TOKEN=token
    POSTGRES_HOST=postgresdb
    POSTGRES_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DATABASE_NAME=postgres
    NINJA_BEARER_TOKEN=supersecret
    APPLIFT_BASE_URL=https://applifting-python-excercise-ms.herokuapp.com/api/v1

### Functionalities

#### Create a product

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/applift/create-product' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer supersecret' \
  -H 'Content-Type: application/json' \
  -d '{
  "product_id": "111",
  "product_name": "string",
  "product_description": "string"
}'
```    
    