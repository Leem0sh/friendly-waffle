# Friendly-waffle

### How to use it

1. `git clone https://github.com/Leem0sh/friendly-waffle.git` to clone the repository
2. `docker build -t friendly-waffle:latest friendly-waffle` to build the image
3. `docker-compose -f friendly-waffle/docker-compose.yaml up -d` to start the containers
4. `docker container ls` and find the `applift-api` `<CONTAINER ID>` to get the container ID
5. `docker exec -it <CONTAINER ID> python manage.py migrate` to create the database
6. visit `http://localhost:8000/api/applift/docs`
7. enjoy

### Secrets - create .env file

    DJANGO_SECRET_KEY=<SECRET KEY>
    SECRET_TOKEN=token
    POSTGRES_HOST=postgresdb
    POSTGRES_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DATABASE_NAME=postgres
    NINJA_BEARER_TOKEN=supersecret
    APPLIFT_BASE_URL=https://applifting-python-excercise-ms.herokuapp.com/api/v1

### Product

#### Create a product (POST)

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/applift/create-product' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer supersecret' \
  -H 'Content-Type: application/json' \
  -d '{
  "product_id": 111,
  "product_name": "string",
  "product_description": "string"
}'
```

#### Get product by ID (GET)

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/applift/get?product_id=111' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer supersecret'
```

#### Update product by ID (PATCH)

```
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/applift/update' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer supersecret' \
  -H 'Content-Type: application/json' \
  -d '{
  "product_id": 111,
  "product_name": "string",
  "product_description": "string"
}'
```

#### Delete product by ID (DELETE)

```
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/applift/delete?product_id=111' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer supersecret'

```

### Offers

#### Get all offers to product (GET)

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/applift/offers/?product_id=111' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer supersecret'
```