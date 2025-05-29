build:
	docker build -t qtravelai/nlp-geocoding-api .

push:
	docker push qtravelai/nlp-geocoding-api

start:
	docker compose up --detach

stop:
	docker compose down