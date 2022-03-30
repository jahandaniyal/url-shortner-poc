.PHONY: build purgedb run stop

build: clean stop purgedb
	mkdir -p 'authservice/.data/db'
	cd authservice; docker-compose up -d --build
	cd urlservice; docker-compose up -d --build
	cd urlservice; docker-compose exec app python utils.py
	- docker network create url-shortner-network
	cd authservice; docker-compose exec backend python manage.py makemigrations
	cd authservice; docker-compose exec backend python manage.py migrate
	cd authservice; docker-compose exec backend python manage.py loaddata init_user_data.json
	cd urlservice; docker-compose kill app db
	cd authservice; docker-compose kill backend db

purgedb:
	echo "Removing all Data from DB"
	- docker rm url_service_db
	- docker rm auth_service_db

clean:
	rm -rf authservice/.data
	rm -rf urlservice/.init-db.js

run:
	cd urlservice; docker-compose up -d --build
	cd authservice; docker-compose up -d --build
	- docker network connect url-shortner-network url_service
	- docker network connect url-shortner-network auth_service

stop:
	cd urlservice; docker-compose kill app db
	cd authservice; docker-compose kill backend db