DB_CONTAINER=household-economics-postgres-server

start-db:
	docker run --name $(DB_CONTAINER) -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres

restart-db:
	docker restart $(DB_CONTAINER)
	docker container logs --follow $(DB_CONTAINER)

stop-db:
	docker stop $(DB_CONTAINER)

create-db:
	psql -h localhost -U postgres -c 'CREATE DATABASE household_economics;'

connect-db:
	psql -h localhost -U postgres -d household_economics

clean-containers:
	docker container rm -f $(DB_CONTAINER)

test:
	python manage.py test -v 2

run:
	python manage.py runserver

create-migration-files:
	python manage.py makemigrations

apply-migration:
	python manage.py migrate