# Friendly-waffle

Apllcation in also deployed on Heroku: https://intense-ravine-66190.herokuapp.com/

### How to use it with docker-compose

1. `git clone https://github.com/Leem0sh/friendly-waffle.git; cd .\friendly-waffle\` to clone the repository
2. create `.env` file
    ```
    DJANGO_SECRET_KEY=<SECRET KEY>
    SECRET_TOKEN=<APPLIFT_TOKEN>
    POSTGRES_HOST=postgresdb
    POSTGRES_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DATABASE_NAME=postgres
    NINJA_BEARER_TOKEN=secrettoken
    APPLIFT_BASE_URL=https://<url>.com
   ```
3. `docker build -t friendly-waffle:latest .` to build the image
4. `docker-compose -f docker-compose.yaml up -d` to start the containers
5. `docker container ls` and find the `applift-api` `<CONTAINER ID>` to get the container ID
6. `docker exec -it <CONTAINER ID> python manage.py migrate` to create the database
7. visit `http://localhost:8000/api/applift/docs`
8. enjoy

### Troubleshooting

Since django-heroku is messing with logging and is not needed for local development,
it is recommended to disable it by commenting it in the settings.py file.

### Product

#### Create a product (POST)

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/applift/create-product' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer secrettoken' \
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
  -H 'Authorization: Bearer secrettoken'
```

#### Get all products (GET)

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/applift/get-all-products' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer secrettoken'
```

#### Update product by ID (PATCH)

```
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/applift/update' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer secrettoken' \
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
  -H 'Authorization: Bearer secrettoken'

```

### Offers

#### Get all offers to product (GET)

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/applift/offers/?product_id=111' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer secrettoken'
```