cowryrise project assesment

# Setting up migration for backend and frontend services

### For Backend Service:
```
export FLASK_APP=backend.app
export APP_ROLE=backend
flask db init --directory backend/migrations
flask db migrate --directory backend/migrations
<!-- flask db migrate -m "Updated book and user relationship" --directory backend/migrations -->
flask db upgrade --directory backend/migrations
```

### For Frontend Service:
```
export FLASK_APP=frontend.app
flask db init --directory frontend/migrations
flask db migrate --directory frontend/migrations
flask db upgrade --directory frontend/migrations
```


### Build Docker
```
sudo docker-compose build 
```

### Starting up docker
```
sudo docker-compose up -d
```