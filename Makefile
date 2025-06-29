IMAGE_NAME = l1romanz/api_545
CONTAINER_NAME = 545api
PORT = 54554

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d -p $(PORT):8000 --name $(CONTAINER_NAME) --restart always \
		-e DB_USER=$${DB_USER} \
		-e DB_PASSWORD=$${DB_PASSWORD} \
		-e DB_HOST=$${DB_HOST} \
		-e DB_PORT=$${DB_PORT} \
		-e DB_NAME=$${DB_NAME} \
		-e SECRET_KEY=$${SECRET_KEY} \
		-e DEBUG=$${DEBUG} \
		$(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)

remove:
	docker rm $(CONTAINER_NAME)

rebuild: stop remove build run

migrate:
	docker exec -it $(CONTAINER_NAME) python manage.py migrate

createsuperuser:
	docker exec -it $(CONTAINER_NAME) python manage.py createsuperuser